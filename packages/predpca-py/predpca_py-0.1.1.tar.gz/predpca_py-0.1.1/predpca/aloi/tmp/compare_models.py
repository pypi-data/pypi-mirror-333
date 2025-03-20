import json
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import torch
from torchvision.utils import save_image

from predpca.aloi.predpca_utils import predict_encoding, preproc_data
from predpca.models.base_encoder import BaseEncoder
from predpca.models.baselines.autoencoder.encoder import AE
from predpca.models.baselines.autoencoder.model import AEModel
from predpca.models.baselines.ltae.encoder import LTAE
from predpca.models.baselines.ltae.model import LTAEModel
from predpca.models.baselines.tae.encoder import TAE
from predpca.models.baselines.tae.model import TAEModel
from predpca.models.baselines.tica.encoder import TICA
from predpca.models.baselines.vae.encoder import VAE
from predpca.models.baselines.vae.model import VAEModel
from predpca.models.ica import ICA
from predpca.models.predpca.encoder import PredPCAEncoder
from predpca.models.predpca.model import PredPCA

# ALOI specific parameters
T_train = 57600  # number of training data
T_test = 14400  # number of test data
Ns = 300  # dimensionality of inputs
Nu = 128  # dimensionality of encoders
Kf_list = [6, 12, 18, 24, 30]  # future timepoints for prediction
WithNoise = False

aloi_dir = Path(__file__).parent
data_dir = aloi_dir / "data"
out_dir = aloi_dir / "output" / "model_comparison"

np.random.seed(1000000)


def main():
    out_dir.mkdir(parents=True, exist_ok=True)
    results = compare_models()

    # save results
    with open(out_dir / "results.json", "w") as f:
        json.dump(results, f, indent=4)

    # Display the results
    for model_name, metrics in results.items():
        print(f"\nResults for {model_name}:")
        for metric_name, value in metrics.items():
            print(f"{metric_name}: {value}")


def compare_models():
    # Load and preprocess data
    print("Loading data...")
    npz = np.load(data_dir / "aloi_data.npz")
    data = npz["data"][:Ns, :].astype(float)  # (Ns, Timg)

    print("Preprocessing data...")
    s_train, s_test, s_target_train, s_target_test = preproc_data(data, T_train, T_test, Kf_list, WithNoise)

    # Prepare encoders
    input_dim = s_train.shape[0]
    encoders = [
        VAE(
            model=VAEModel(units=[input_dim, 200, 150, Nu]),
            epochs=10,
        ),
        AE(
            model=AEModel(units=[input_dim, 200, 150, Nu]),
            epochs=10,
        ),
        PredPCAEncoder(
            model=PredPCA(
                kp_list=range(0, 37, 2),
                prior_s_=100,
            ),
            Ns=Ns,
            Nu=Nu,
        ),
        TAE(
            model=TAEModel(units=[input_dim, 200, 150, Nu]),
            epochs=10,
        ),
        TICA(
            dim=Nu,
        ),
        LTAE(
            model=LTAEModel(n_components=Nu),
        ),
    ]

    # Evaluate encoders
    results = {}

    for encoder in encoders:
        results[encoder.name] = evaluate_encoder(encoder, s_train.T, s_test.T, s_target_test)

    return results


def evaluate_encoder(
    encoder: BaseEncoder,
    input_train: np.ndarray,
    input_test: np.ndarray,
    target_train: np.ndarray,
    target_test: np.ndarray,
) -> dict[str, float]:
    """Evaluate a single encoder using prediction error metrics"""
    print(f"\nEvaluating {encoder.name}...")
    start_time = time.time()

    # Center the data
    # input_mean = input_train.mean(axis=0, keepdims=True)
    # input_train_centered = input_train - input_mean
    # input_test_centered = input_test - input_mean
    input_mean = 0

    # Encode
    encoder.fit(input_train, target_train)
    test_encodings = encoder.encode(input_test)

    # Compute reconstruction error if decoder is available
    metrics = {}
    if hasattr(encoder, "decode"):
        reconst = encoder.decode(test_encodings) + input_mean
        mse = np.mean((reconst - input_test) ** 2)
        metrics["reconstruction_mse"] = float(mse)

        # Visualize reconstructions
        visualize_decodings(input_test, reconst, out_dir / f"{encoder.name.lower()}_decodings.png")

    # Plot learning curves if available
    if hasattr(encoder, "train_losses") and hasattr(encoder, "val_losses"):
        train_steps, train_losses = encoder.train_losses
        val_steps, val_losses = encoder.val_losses
        fig = plot_losses(train_steps, train_losses, val_steps, val_losses)
        fig.savefig(out_dir / f"{encoder.name.lower()}_losses.png")
        plt.close(fig)

    metrics["computation_time"] = time.time() - start_time
    return metrics


def visualize_decodings(input_data: np.ndarray, reconst_data: np.ndarray, filename: str, n_samples: int = 10):
    """Visualize original and reconstructed images side by side"""
    comparison = np.concatenate(
        [input_data[:n_samples].reshape(-1, 1, Ns), reconst_data[:n_samples].reshape(-1, 1, Ns)], axis=0
    )
    save_image(torch.from_numpy(comparison), filename, nrow=n_samples)


def plot_losses(
    train_steps: np.ndarray,
    train_losses: np.ndarray,
    val_steps: np.ndarray,
    val_losses: np.ndarray,
):
    """Plot training and validation losses"""
    fig = plt.figure()
    plt.plot(train_steps, train_losses, label="Training Loss")
    plt.plot(val_steps, val_losses, label="Validation Loss", marker="o")
    plt.legend()
    plt.xlabel("Step")
    plt.ylabel("Loss")
    return fig


if __name__ == "__main__":
    main()
