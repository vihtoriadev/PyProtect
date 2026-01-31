
import base64
import marshal
import zlib
from pathlib import Path

from src.tools import ToolsConsole


class Obfuscator:
    def __init__(self, input_file: Path, output_file: Path, obf_method: str, compress: bool = False):
        self.input_file = input_file
        self.output_file = output_file
        self.obf_method = obf_method
        self.compress = compress

        self.methods = {
            "--bytecode": self._obfuscate_bytecode,
        }

    def obfuscate(self):
        if self.obf_method not in self.methods:
            return False, ToolsConsole.error(f"Obfuscation method '{self.obf_method}' is not supported.")
        
        return self.methods[self.obf_method]()

    def _obfuscate_bytecode(self):
        try:
            LOADER_TEMPLATE = '''import base64 as b, marshal as m{decompress_import};a={b64!s};b=b.b64decode(a){maybe_decompress};c=m.loads(b);exec(c)''' 
            src = ToolsConsole.read_file(self.input_file)
            code_obj = compile(src, str(self.output_file), "exec")

            data = marshal.dumps(code_obj)

            if self.compress:
                data = zlib.compress(data)
                
            b64 = base64.b64encode(data).decode("ascii")

            loader = LOADER_TEMPLATE.format(
                b64=repr(b64),
                decompress_import=";import zlib as z" if self.compress else "",
                maybe_decompress=";b=z.decompress(b)" if self.compress else ""
            )

            return True, loader
        
        except Exception as e:
            return False, str(e)
        
