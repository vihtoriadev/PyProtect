
from typing import Set

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Arguments:
    ARGUMENTS: Set[str] = {
        '--help', '-h',
        '--input', '-in',
        '--output', '-out',
        '--bytecode',
        '--compress',
    }

    OBFISCATION_METHODS: Set[str] = {
        '--bytecode',
    }


class ToolsConsole:
    @staticmethod
    def warn(message: str):
        print(f"{bcolors.WARNING}[!]{bcolors.RESET} {message}")

    @staticmethod
    def info(message: str):
        print(f"{bcolors.OKGREEN}[+]{bcolors.RESET} {message}")

    @staticmethod
    def error(message: str):
        print(f"{bcolors.FAIL}[-]{bcolors.RESET} {message}")

    @staticmethod
    def success(message: str):
        print(f"{bcolors.OKBLUE}[OK]{bcolors.RESET} {message}")

    @staticmethod
    def validate_args(args: list) -> bool:
        for arg in args:
            if arg.startswith('-') and arg not in Arguments.ARGUMENTS:
                return False
        return True

    @staticmethod
    def usage():
        print(
            "Usage: pyprotect.py [options]"
            "\n"
            "\nOptions:"
            "\n    --help, -h                Show this help message and exit."
            "\n    --input, -in FILE         Input .py file"
            "\n    --output, -out FILE       Output .py file (default: obfuscated_<input>)"
            "\n"
            "\nObfuscation options:"
            "\n    --bytecode            Obfuscate using marshal bytecode loader"
            "\n        --compress        Apply zlib.compress before base64 (recommended)"
            "\n                              (valid only when --bytecode is set)"
            "\n"
            "\nExamples:"
            "\n    pyprotect.py --input <input_file> --output <output_file> <obfuscation_option>"
        )

    @staticmethod
    def read_file(input_path: str) -> str:
        with open(input_path, 'r', encoding='utf-8') as f:
            return f.read()
        return ""

    @staticmethod
    def save_file(code: str, output_path: str):
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(code)
                ToolsConsole.success(f"File saved to '{output_path}'.")
        except Exception:
            ToolsConsole.error(f"Failed to save file to '{output_path}'.")