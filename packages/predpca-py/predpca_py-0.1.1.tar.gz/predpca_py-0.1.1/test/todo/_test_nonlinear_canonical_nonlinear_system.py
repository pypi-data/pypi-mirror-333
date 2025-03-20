from pathlib import Path

import numpy as np

from predpca.nonlinear.canonical_nonlinear_system import canonical_nonlinear_system


def test_nonlinear_canonical_nonlinear_system():
    np.random.seed(1000000)
    (
        x_train,
        x_test,
        psi_train,
        psi_test,
    ) = canonical_nonlinear_system(
        Nx=10,
        Npsi=100,
        T_train=100000,
        T_test=100000,
        sigma_z=0.001,
    )

    npz = np.load(Path(__file__).parent / "supplfig1/canonical_nonlinear_system_py.npz")
    atol = 0
    np.testing.assert_allclose(x_train, npz["x"], atol=atol)
    np.testing.assert_allclose(x_test, npz["x2"], atol=atol)
    np.testing.assert_allclose(psi_train, npz["psi"], atol=atol)
    np.testing.assert_allclose(psi_test, npz["psi2"], atol=atol)
    # np.testing.assert_allclose(z_train, npz["z"], atol=atol)
    # np.testing.assert_allclose(z_test, npz["z2"], atol=atol)
    # np.testing.assert_allclose(R, npz["R"], atol=atol)
    # np.testing.assert_allclose(B, npz["B"], atol=atol)
    # np.testing.assert_allclose(meanx0, npz["meanx0"], atol=atol)


if __name__ == "__main__":
    test_nonlinear_canonical_nonlinear_system()
    print("All tests passed!")
