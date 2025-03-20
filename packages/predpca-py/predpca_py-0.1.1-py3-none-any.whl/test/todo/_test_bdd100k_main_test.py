from pathlib import Path

import numpy as np

from predpca.bdd100k.main_test import main


def _test_bdd100k_main_test():
    data_dir = Path("/mnt/ms-nas-2/yoshida/predpca/bdd100k/sample_8x_5s")

    main(
        preproc_out_dir=data_dir,
        train_out_dir=data_dir,
    )

    py_dir = data_dir / "output_python"
    pynic_dir = data_dir / "output"

    npz_py = np.load(py_dir / "predpca_lv1_dst.npz")
    npz_pynic = np.load(pynic_dir / "predpca_lv1_dst.npz")
    atol = 1e-2
    np.testing.assert_allclose(npz_py["PPCA_C1t"], npz_pynic["PPCA_C1t"], atol=atol)
    np.testing.assert_allclose(npz_py["PPCA_L1t"], npz_pynic["PPCA_L1t"], atol=atol)
    np.testing.assert_allclose(npz_py["PPCA_C1b"], npz_pynic["PPCA_C1b"], atol=atol)
    np.testing.assert_allclose(npz_py["PPCA_L1b"], npz_pynic["PPCA_L1b"], atol=atol)

    npz_py = np.load(py_dir / "predpca_lv1_u_1.npz")
    npz_pynic = np.load(pynic_dir / "predpca_lv1_u_1.npz")
    atol = 1e-2
    np.testing.assert_allclose(npz_py["u"], npz_pynic["u"], atol=atol)

    csv_py = np.loadtxt(py_dir / "predpca_test_prediction_error.csv")
    csv_pynic = np.loadtxt(pynic_dir / "predpca_test_prediction_error.csv")
    atol = 1e-2
    np.testing.assert_allclose(csv_py, csv_pynic, atol=atol)


if __name__ == "__main__":
    _test_bdd100k_main_test()
    print("All tests passed!")
