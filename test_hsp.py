import hsp_package


class TestClass:
    def test_one(self):
        assert hsp_package.c1([1, 2, 3]) == 1

    def test_two(self):
        assert (
            hsp_package.SumSqr(
                hsp_package.np.array([3, 4]), hsp_package.np.array([0, 0])
            )
            == 25
        )

    def test_three(self):
        assert hsp_package.Equal1([0.5, 0.25, 0]) == 0.25
