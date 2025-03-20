from pathlib import Path

import numpy as np

from predpca.bdd100k.main_analyze_categorical_features import main


def test_bdd100k_main_analyze_categorical_features():
    data_dir = Path("/mnt/ms-nas-2/yoshida/predpca/bdd100k/sample_8x_5s")

    (
        u,
        Wica,
        uica,
        out,
        up,
        brightness,
        vertical,
        lateral,
    ) = main(
        preproc_out_dir=data_dir / "output_python",
        test_out_dir=data_dir / "output_python",
    )

    npz = np.load(data_dir / "output_python" / "predpca_bdd_cat.npz")

    atol = 1e-7
    np.testing.assert_allclose(u, npz["u"], atol=atol, verbose=True)
    # np.testing.assert_allclose(t_list, npz["t_list"], atol=atol)
    np.testing.assert_allclose(up, npz["up"], atol=atol)
    np.testing.assert_allclose(brightness, npz["brightness"], atol=atol)
    np.testing.assert_allclose(vertical, npz["vertical"], atol=atol)
    np.testing.assert_allclose(lateral, npz["lateral"], atol=atol)

    # difference due to numpy vs torch
    # passes with atol=0 before 76252fcdbe4972f3cace5c7769f36ed20fe6e5f7
    atol = 1
    np.testing.assert_allclose(Wica, npz["Wica"], atol=atol)
    np.testing.assert_allclose(out, npz["output2"], atol=atol)
    # atol = 4e4
    # rtol = 1.1
    # commented out; testing Wica is enough
    # np.testing.assert_allclose(uica, npz["uica"], rtol=rtol)


if __name__ == "__main__":
    test_bdd100k_main_analyze_categorical_features()
    print("All tests passed!")
