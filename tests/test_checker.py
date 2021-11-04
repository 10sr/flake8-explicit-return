"""Test NIC Chekcer."""

import ast
import tokenize
import unittest

from io import BytesIO
from typing import Iterable
from typing import Tuple

from flake8_explicit_return import Checker


def _tokenize(input_: str) -> Iterable[tokenize.TokenInfo]:
    return tokenize.tokenize(BytesIO(input_.encode("utf-8")).readline)


class TestChecker(unittest.TestCase):
    """Test NIC Chekcer."""

    def test_noerror(self) -> None:
        """Test checker with valid input."""
        input_ = "".join(
            [
                """def f1(a):\n""",
                """    a = a + "hoe"\n""",
                """    return a\n""",
            ]
        )
        checker = Checker(ast.parse(input_), _tokenize(input_))
        actual = list(checker.run())
        expected = []  # type: Iterable[Tuple[int, int, str, None]]
        self.assertEqual(actual, expected)
        return

    def test_error(self) -> None:
        """Test checker with invalid input."""
        # More test cases are defined in run_flake8/Run.sh script
        input_ = "".join(
            [
                """def f1(a):\n""",
                """    a = a + "hoe"\n""",
                """    print(a)\n""",
            ]
        )
        checker = Checker(ast.parse(input_), _tokenize(input_))
        actual = list(checker.run())
        expected = [
            (3, 4, "XRT001 Function must end with bare return or raise statement", None)
        ]
        self.assertEqual(actual, expected)
        return


if __name__ == "__main__":
    unittest.main()
