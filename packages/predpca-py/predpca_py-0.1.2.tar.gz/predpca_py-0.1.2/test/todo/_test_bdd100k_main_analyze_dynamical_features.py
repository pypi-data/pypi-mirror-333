from pathlib import Path

import numpy as np

from predpca.bdd100k.main_analyze_dynamical_features import main


def test_bdd100k_main_analyze_dynamical_features():
    data_dir = Path("/mnt/ms-nas-2/yoshida/predpca/bdd100k/sample_8x_5s")

    (
        u,
        Wica,
        uica,
        out,
        up,
        lateral_motion,
    ) = main(
        preproc_out_dir=data_dir / "output_python",
        test_out_dir=data_dir / "output_python",
    )

    npz = np.load(data_dir / "output_python" / "predpca_bdd_dyn.npz")

    atol = 0
    np.testing.assert_allclose(u, npz["u"], atol=atol, verbose=True)
    # np.testing.assert_allclose(t_list, npz["t_list"], atol=atol)
    np.testing.assert_allclose(up, npz["up"], atol=atol)
    np.testing.assert_allclose(lateral_motion, npz["lateral_motion"], atol=atol)

    # difference due to numpy vs torch
    atol = 1.1
    np.testing.assert_allclose(Wica, npz["Wica"], atol=atol)
    np.testing.assert_allclose(out, npz["output2"], atol=atol)
    atol = 1e3
    np.testing.assert_allclose(uica, npz["uica"], atol=atol)


if __name__ == "__main__":
    test_bdd100k_main_analyze_dynamical_features()
    print("All tests passed!")
