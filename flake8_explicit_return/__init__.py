"""Flake8 plugin XRT."""

import ast
import tokenize

from typing import Iterable
from typing import Tuple

from ._version import __version__

_ERROR = Tuple[int, int, str, None]


def _check(root: ast.AST) -> Iterable[_ERROR]:
    for node in ast.walk(root):
        if not isinstance(node, ast.FunctionDef):
            continue
        body_last = node.body[-1]
        if not (isinstance(body_last, ast.Return) or isinstance(body_last, ast.Raise)):
            yield (
                body_last.lineno,
                body_last.col_offset,
                "XRT001 Function must end with bare return or raise statement",
                None,
            )
    return


class Checker:
    """XRT Checker definition."""

    name = "explicit-return"
    version = __version__

    def __init__(self, tree: ast.AST, file_tokens: Iterable[tokenize.TokenInfo]):
        """Intialize Checker.

        :param tree: File AST
        :param file_tokens: File tokens
        """
        self.tree = tree
        self.file_tokens = file_tokens
        return

    def run(self) -> Iterable[_ERROR]:
        """Run checker.

        :yields: Errors found.
        """
        yield from _check(self.tree)
        return
