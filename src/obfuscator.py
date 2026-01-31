import base64
import marshal
import zlib
import random
import string
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
            "--lambda": self._obfuscate_lambda,
            "--hybrid": self._obfuscate_hybrid,
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
    
    def _generate_random_name(self, length: int = 10) -> str:
        return ''.join(random.choices(string.ascii_lowercase, k=length))
    
    def _obfuscate_lambda(self):
        try:
            src = ToolsConsole.read_file(self.input_file)
            
            encoded = base64.b64encode(src.encode('utf-8')).decode('ascii')
            
            if self.compress and len(encoded) > 100:
                num_parts = random.randint(3, 5)
                parts = []
                chunk_size = len(encoded) // num_parts
                
                for i in range(num_parts):
                    if i == num_parts - 1:
                        parts.append(encoded[i * chunk_size:])
                    else:
                        parts.append(encoded[i * chunk_size:(i + 1) * chunk_size])
                
                encoded_str = '+'.join([repr(p) for p in parts])
            else:
                encoded_str = repr(encoded)
            
            v1 = self._generate_random_name()
            v2 = self._generate_random_name()
            v3 = self._generate_random_name()
            v4 = self._generate_random_name()
            v5 = self._generate_random_name()
            v6 = self._generate_random_name()

            LAMBDA_TEMPLATE = f'''(lambda {v1}: (lambda {v2}: (lambda {v3}: (lambda {v4}: {v4}({v3}({v2}({v1}))))(lambda {v5}: exec({v5})))(lambda {v5}: {v5}.decode('utf-8')))(lambda {v5}: __import__('base64').b64decode({v5})))({encoded_str})'''

            return True, LAMBDA_TEMPLATE
            
        except Exception as e:
            return False, str(e)
        
    def _obfuscate_hybrid(self):
        try:
            src = ToolsConsole.read_file(self.input_file)

            code_obj = compile(src, str(self.output_file), "exec")
            data = marshal.dumps(code_obj)

            if self.compress:
                data = zlib.compress(data)

            encoded = base64.b64encode(data).decode("ascii")

            if len(encoded) > 120:
                num_parts = random.randint(3, 6)
                chunk_size = len(encoded) // num_parts
                parts = [
                    encoded[i * chunk_size:] if i == num_parts - 1
                    else encoded[i * chunk_size:(i + 1) * chunk_size]
                    for i in range(num_parts)
                ]
                encoded_str = '+'.join(repr(p) for p in parts)
            else:
                encoded_str = repr(encoded)

            v1 = self._generate_random_name()
            v2 = self._generate_random_name()
            v3 = self._generate_random_name()
            v4 = self._generate_random_name()
            v5 = self._generate_random_name()
            v6 = self._generate_random_name()

            LAMBDA_TEMPLATE = f'''(lambda {v1}: (lambda {v2}: (lambda {v3}: (lambda {v4}: {v4}({v3}({v2}({v1}))))(lambda {v5}: __import__('builtins').exec(__import__('marshal').loads({v5}))))(lambda {v5}: __import__('zlib').decompress({v5}) if {self.compress} else {v5}))(lambda {v5}: __import__('base64').b64decode({v5})))({encoded_str})'''

            return True, LAMBDA_TEMPLATE

        except Exception as e:
            return False, str(e)
