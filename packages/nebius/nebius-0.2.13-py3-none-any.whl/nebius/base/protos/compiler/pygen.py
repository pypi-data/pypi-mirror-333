import io
from collections.abc import Sequence
from keyword import iskeyword, issoftkeyword
from types import TracebackType
from typing import Any, Literal, TextIO

GENERATED_NOTE = """
Generated by the nebius.base.protos.compiler.  DO NOT EDIT!
"""


class GenerationError(Exception):
    pass


class ImportPath:
    def __init__(self, import_path: str, suggest_name: str | None = None) -> None:
        self.import_path = import_path
        self.suggest_name = suggest_name

    def __eq__(self, value: object) -> bool:
        if isinstance(value, ImportPath) and value.import_path == self.import_path:
            return True
        if isinstance(value, str) and value == self.import_path:
            return True
        return False


class ImportedSymbol:
    def __init__(self, name: str, import_path: ImportPath | str) -> None:
        self.name = name
        self.import_path = (
            import_path
            if isinstance(import_path, ImportPath)
            else ImportPath(import_path)
        )

    def __eq__(self, value: object) -> bool:
        if (
            isinstance(value, ImportedSymbol)
            and value.import_path == self.import_path
            and value.name == self.name
        ):
            return True
        return False

    def as_type_hint(self) -> "TypeHint":
        return TypeHint(self.name, self.import_path)


class TypeHint(ImportedSymbol):
    def as_symbol(self) -> ImportedSymbol:
        return ImportedSymbol(self.name, self.import_path)


Token = str | TypeHint | ImportedSymbol | ImportPath | Any


class PyGenFile:
    def __init__(
        self,
        import_path: str | ImportPath,
        indent_sequence: str | None = None,
        shebang_command: str | None = None,
        generated_note: str | None = None,
        used_names: Sequence[str] | None = None,
    ) -> None:
        self._shebang_command = shebang_command
        self._generated_note = (
            generated_note if generated_note is not None else GENERATED_NOTE
        )
        self._import_path = (
            import_path if isinstance(import_path, str) else import_path.import_path
        )
        self._used_names = set(used_names) if used_names is not None else set[str]()
        self._main_code = io.StringIO("")
        self._imports = dict[str, ImportPath]()
        self._imports_reversed = dict[str, str]()
        self._indent_sequence = (
            indent_sequence if indent_sequence is not None else "    "
        )
        self._indent = 0
        self._finalized = False

    def is_local(self, import_path: ImportPath | str) -> bool:
        import_path_str = (
            import_path.import_path
            if isinstance(import_path, ImportPath)
            else import_path
        )
        return import_path_str == self._import_path

    def append_used_names(self, used_names: Sequence[str]) -> None:
        self._used_names = self._used_names.union(used_names)

    def suggest_name(
        self,
        suggestion: str,
        additional_names: Sequence[str] | None = None,
    ) -> str:
        ans = set(additional_names) if additional_names is not None else set[str]()

        def is_reserved(s: str) -> bool:
            return (
                s in self._imports_reversed
                or s in self._used_names
                or s in ans
                or iskeyword(s)
                or issoftkeyword(s)
            )

        if is_reserved(suggestion):
            inc = 1
            while True:
                new_suggest_name = f"{suggestion}_{inc}"
                if not is_reserved(new_suggest_name):
                    break
                inc += 1
            return new_suggest_name
        else:
            return suggestion

    def add_import(
        self,
        import_path: ImportPath | str,
        suggest_name: str | None = None,
    ) -> ImportPath:
        if self._finalized:
            GenerationError("can't add imports to finalized file")
        import_path_str = (
            import_path.import_path
            if isinstance(import_path, ImportPath)
            else import_path
        )
        if self.is_local(import_path):
            return ImportPath(import_path_str)
        if import_path_str in self._imports:
            return self._imports[import_path_str]
        if suggest_name is None and isinstance(import_path, ImportPath):
            suggest_name = import_path.suggest_name
        if suggest_name is None:
            suggest_name = import_path_str.split(".")[-1]
        if not isinstance(import_path, ImportPath):
            import_path = ImportPath(import_path, suggest_name)

        suggest_name = self.suggest_name(suggest_name)

        import_path = ImportPath(import_path.import_path, suggest_name)
        self._imports[import_path.import_path] = import_path
        self._imports_reversed[suggest_name] = import_path.import_path
        return import_path

    def indent(self) -> None:
        if self._finalized:
            GenerationError("can't indent finalized file")
        self._indent += 1

    def unindent(self) -> None:
        if self._indent <= 0:
            raise GenerationError("can't unindent more")
        self._indent -= 1

    def __enter__(self) -> "PyGenFile":
        self.indent()
        return self

    def __exit__(
        self,
        type_: type[BaseException] | None,
        value: BaseException | None,
        traceback: TracebackType | None,
    ) -> Literal[False]:
        self.unindent()
        return False

    def p(
        self,
        *args: Token,
        noindent: bool = False,
        add_eol: bool = True,
    ) -> None:
        if self._finalized:
            GenerationError("can't add lines to finalized file")
        if not noindent:
            self._main_code.write("".join([self._indent_sequence] * self._indent))
        for arg in args:
            if isinstance(arg, TypeHint):
                if self.is_local(arg.import_path):
                    self._main_code.write('"')
                    self._main_code.write(arg.name)
                    self._main_code.write('"')
                else:
                    import_path = self.add_import(arg.import_path)
                    self._main_code.write(str(import_path.suggest_name))
                    self._main_code.write(".")
                    self._main_code.write(arg.name)
            elif isinstance(arg, ImportedSymbol):
                if self.is_local(arg.import_path):
                    self._main_code.write(arg.name)
                else:
                    import_path = self.add_import(arg.import_path)
                    self._main_code.write(str(import_path.suggest_name))
                    self._main_code.write(".")
                    self._main_code.write(arg.name)
            elif isinstance(arg, ImportPath):
                if self.is_local(arg):
                    raise GenerationError(
                        f"can't add import path {arg.import_path} as an import to"
                        " itself"
                    )
                import_path = self.add_import(arg.import_path)
                self._main_code.write(str(import_path.suggest_name))
            else:
                self._main_code.write(f"{arg}")
        if add_eol:
            self._main_code.write("\n")

    def dump(self, writer: TextIO) -> None:
        self._finalized = True
        if self._shebang_command is not None:
            writer.write("#!")
            writer.write(self._shebang_command)
            writer.write("\n")
        gen_note = self._generated_note.split("\n")
        for line in gen_note:
            writer.write("# ")
            writer.write(line)
            writer.write("\n")
        writer.write("\n")
        for _imp in self._imports.values():
            writer.write("import ")
            writer.write(_imp.import_path)
            writer.write(" as ")
            writer.write(str(_imp.suggest_name))
            writer.write("\n")
        writer.write("#@ local imports here @#")
        writer.write("\n")
        writer.write("\n")
        writer.write(self._main_code.getvalue())
        writer.flush()

    def dumps(self) -> str:
        ret = io.StringIO("")
        self.dump(ret)
        return ret.getvalue()
