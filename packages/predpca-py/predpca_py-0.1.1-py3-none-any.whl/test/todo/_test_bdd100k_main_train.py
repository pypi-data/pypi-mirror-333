from pathlib import Path

import numpy as np

from predpca.bdd100k.main_train import main


def test_bdd100k_main_train():
    data_dir = Path("/mnt/ms-nas-2/yoshida/predpca/bdd100k/sample_8x_5s")

    main(
        preproc_out_dir=data_dir,
        overwrite=True,
    )

    py_dir = data_dir / "output_python"
    npz_py = np.load(py_dir / "mle_lv1_00.npz")
    pynic_dir = data_dir / "output"
    npz_pynic = np.load(pynic_dir / "mle_lv1_00.npz")

    atol = 0
    np.testing.assert_allclose(npz_py["Tpart_t"], npz_pynic["Tpart_t"], atol=atol)
    np.testing.assert_allclose(npz_py["Tpart_b"], npz_pynic["Tpart_b"], atol=atol)

    atol = 1e-3
    for i in range(6):
        np.testing.assert_allclose(npz_py[f"STS_t{i + 1}"], npz_pynic["STS_t"][i], atol=atol)
        np.testing.assert_allclose(npz_py[f"S_S_t{i + 1}"], npz_pynic["S_S_t"][i], atol=atol)
        np.testing.assert_allclose(npz_py[f"STS_b{i + 1}"], npz_pynic["STS_b"][i], atol=atol)
        np.testing.assert_allclose(npz_py[f"S_S_b{i + 1}"], npz_pynic["S_S_b"][i], atol=atol)


if __name__ == "__main__":
    test_bdd100k_main_train()
    print("All tests passed!")
