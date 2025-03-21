from jupyter2pytest.extractor import open_notebook, extract_with_prefix
from jupyter2pytest.compiler import compile_code_and_tests_into_py

import sys

if __name__ == "__main__":
    code_file = sys.argv[1]
    test_pattern = sys.argv[2]
    out_file = sys.argv[3]

    code = open_notebook(code_file)

    code_blocks = extract_with_prefix(code, test_pattern)

    tester_code = compile_code_and_tests_into_py(code_blocks)

    with open(out_file, "w") as f:
        f.write(tester_code)
