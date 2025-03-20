from pathlib import Path

import numpy as np

from predpca.bdd100k.main_preprocess import main

out_dir = Path(__file__).parent / "fig4_preprocess"
out_dir.mkdir(parents=True, exist_ok=True)


def test_bdd100k_main_preprocess():
    data_dir = Path("/mnt/ms-nas-2/yoshida/predpca/bdd100k/sample_8x_5s")
    main(overwrite=True)

    py_dir = data_dir / "output_python"
    npz_py = np.load(py_dir / "pca_lv1_dst.npz")
    pynic_dir = data_dir / "output"
    npz_pynic = np.load(pynic_dir / "pca_lv1_dst.npz")

    np.testing.assert_allclose(npz_py["mean1"], npz_pynic["mean1"], atol=1e-5)
    np.testing.assert_allclose(npz_py["PCA_C1"], npz_pynic["PCA_C1"], atol=1e-2)  # pcacov is sensitive
    np.testing.assert_allclose(npz_py["PCA_L1"], npz_pynic["PCA_L1"], atol=1e-4)
    np.testing.assert_allclose(npz_py["T"], npz_pynic["T"], atol=0)


if __name__ == "__main__":
    test_bdd100k_main_preprocess()
    print("All tests passed!")
