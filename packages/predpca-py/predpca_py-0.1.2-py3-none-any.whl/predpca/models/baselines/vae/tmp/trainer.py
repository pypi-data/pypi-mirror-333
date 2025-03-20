from typing import Optional

import torch
from torch import nn, optim
from torch.nn import functional as F
from torch.utils.data import DataLoader


def loss_function(recon_x: torch.Tensor, x: torch.Tensor, mu: torch.Tensor, logvar: torch.Tensor) -> torch.Tensor:
    """
    Calculate the loss function for VAE
    Args:
        recon_x: Reconstructed input
        x: Original input
        mu: Mean of the latent variables
        logvar: Log variance of the latent variables

    Returns:
        Total loss value (BCE + KLD)
    """
    # Reconstruction loss
    BCE = F.binary_cross_entropy(recon_x, x.view(-1, 784), reduction="sum")

    # KL divergence
    # see Appendix B from VAE paper:
    # Kingma and Welling. Auto-Encoding Variational Bayes. ICLR, 2014
    # https://arxiv.org/abs/1312.6114
    KLD = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())

    return BCE + KLD


def train_vae(
    model: nn.Module,
    train_loader: DataLoader,
    epochs: int,
    device: torch.device,
    log_interval: int = 10,
    optimizer: Optional[torch.optim.Optimizer] = None,
) -> None:
    """
    Train the VAE model
    Args:
        model: VAE model
        train_loader: DataLoader for training data
        epochs: Number of epochs
        device: Device to use for computation
        log_interval: Interval for logging training progress
        optimizer: Optimizer (uses Adam if None)
    """
    if optimizer is None:
        optimizer = optim.Adam(model.parameters(), lr=1e-3)

    model.train()
    for epoch in range(1, epochs + 1):
        train_loss = 0
        for batch_idx, (data, _) in enumerate(train_loader):
            data = data.to(device)
            optimizer.zero_grad()

            # Forward pass
            recon_batch, mu, logvar = model(data)

            # Calculate loss
            loss = loss_function(recon_batch, data, mu, logvar)

            # Backward pass
            loss.backward()
            train_loss += loss.item()
            optimizer.step()

            # Display training progress
            if batch_idx % log_interval == 0:
                print(
                    "Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}".format(
                        epoch,
                        batch_idx * len(data),
                        len(train_loader.dataset),
                        100.0 * batch_idx / len(train_loader),
                        loss.item() / len(data),
                    )
                )

        # Display average loss for the epoch
        avg_loss = train_loss / len(train_loader.dataset)
        print(f"====> Epoch: {epoch} Average loss: {avg_loss:.4f}")
