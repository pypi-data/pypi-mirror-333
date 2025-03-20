import ast
import inspect
from textwrap import dedent

from melvin.tecton_gen_ai.utils.code_parser import get_declaration


def test_get_declaration():
    def f1(a: int, b: str) -> str:
        return a + b

    def f1_(a: int, b: str) -> str:
        pass

    def f2(a: int, b: str) -> str:
        """
        This is a docstring
        """
        return a + b

    def f2_(a: int, b: str) -> str:
        """
        This is a docstring
        """
        pass

    class F3:
        """
        doc
        """

        def __init__(self, a: int, b: str):
            self.a = a
            self.b = b

        def get_a(self) -> int:
            return self.a

        def get_b(self) -> str:
            """
            This is a docstring
            """
            return self.b

        def _private(self) -> int:
            return 1

    class F3_:
        """
        doc
        """

        def __init__(self, a: int, b: str):
            pass

        def get_a(self) -> int:
            pass

        def get_b(self) -> str:
            """
            This is a docstring
            """
            pass

    class F3_2_:
        """
        doc
        """

        def __init__(self, a: int, b: str):
            pass

    assert get_declaration(f1, entrypoint_only=True).replace(
        "f1", "f1_"
    ) == ast.unparse(ast.parse(dedent(inspect.getsource(f1_))))

    assert get_declaration(f1, entrypoint_only=False).replace(
        "f1", "f1_"
    ) == ast.unparse(ast.parse(dedent(inspect.getsource(f1_))))

    assert get_declaration(f2, entrypoint_only=True).replace(
        "f2", "f2_"
    ) == ast.unparse(ast.parse(dedent(inspect.getsource(f2_))))

    assert get_declaration(f2, entrypoint_only=False).replace(
        "f2", "f2_"
    ) == ast.unparse(ast.parse(dedent(inspect.getsource(f2_))))

    assert get_declaration(F3, entrypoint_only=False).replace(
        "F3", "F3_"
    ) == ast.unparse(ast.parse(dedent(inspect.getsource(F3_))))

    assert get_declaration(F3, entrypoint_only=True).replace(
        "F3", "F3_2_"
    ) == ast.unparse(ast.parse(dedent(inspect.getsource(F3_2_))))
