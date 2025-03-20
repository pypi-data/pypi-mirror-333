from pathlib import Path

import numpy as np

from predpca.nonlinear.lorenz_attractor import lorenz_attractor


def test_nonlinear_lorenz_attractor():
    np.random.seed(1000000)
    (
        x_train,
        x_test,
    ) = lorenz_attractor(
        Nx=3,
        T_train=100000,
        T_test=100000,
    )

    npz = np.load(Path(__file__).parent / "supplfig1/lorenz_attractor_py.npz")
    atol = 0
    np.testing.assert_allclose(x_train, npz["x"], atol=atol)
    np.testing.assert_allclose(x_test, npz["x2"], atol=atol)


if __name__ == "__main__":
    test_nonlinear_lorenz_attractor()
    print("All tests passed!")
