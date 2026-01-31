# PyProtect - Python Code Obfuscator

This tool simplifies the process of obfuscating Python scripts to protect source code from reverse engineering and unauthorized analysis. It enables developers to secure their intellectual property by transforming readable Python code into obfuscated versions that maintain full functionality while being significantly harder to understand and decompile.

## Overview

The script leverages Python's built-in compilation and encoding capabilities to create multiple layers of obfuscation. It supports bytecode conversion using marshal, optional compression with zlib, and base64 encoding to hide the original source code structure. This makes it particularly valuable for developers distributing proprietary software, protecting algorithms, or securing sensitive business logic embedded in Python applications.

```
Usage: pyprotect.py [options]
```

```
Options:
    --help, -h                Show this help message and exit.
    --input, -in FILE         Input .py file
    --output, -out FILE       Output .py file (default: obfuscated_<input>)

Obfuscation options:
    --bytecode            Obfuscate using marshal bytecode loader
        --compress        Apply zlib.compress before base64 (recommended)
                              (valid only when --bytecode is set)

Examples:
    pyprotect.py --input test.py --output obf_test.py --bytecode
    pyprotect.py --input test.py --output obf_test.py --bytecode --compress
```

## How It Works

The obfuscation process is automated through a command-line interface that handles the transformation:

1. **Input Validation**: The tool verifies that the input file exists and has a .py extension.

2. **Compilation**: The Python source code is compiled into bytecode using the compile() function.

3. **Marshalling**: The bytecode object is serialized using marshal.dumps() to create a binary representation.

4. **Compression (Optional)**: When the --compress flag is used, zlib compression is applied to reduce size and add an additional obfuscation layer.

5. **Encoding**: The binary data is encoded to base64 for safe embedding in a Python loader script.

6. **Loader Generation**: A compact loader template is created that reverses the process at runtime, decoding and executing the original code.

## Key Features

- **Bytecode Obfuscation**: Converts Python source to compiled bytecode, removing all comments and formatting
- **Optional Compression**: Reduces file size while adding complexity to reverse engineering attempts
- **Preserves Functionality**: Obfuscated code executes identically to the original
- **Simple Command-Line Interface**: Easy-to-use options for quick obfuscation
- **Minimal Dependencies**: Uses only Python standard library modules (base64, marshal, zlib)
- **Cross-Platform Compatible**: Works on any system with Python 3.x installed

This tool is ideal for developers who need to distribute Python applications while protecting proprietary algorithms, prevent casual source code inspection, or add a layer of security to commercially distributed Python software. While obfuscation is not a substitute for proper encryption or security measures, it significantly raises the barrier for reverse engineering attempts.
