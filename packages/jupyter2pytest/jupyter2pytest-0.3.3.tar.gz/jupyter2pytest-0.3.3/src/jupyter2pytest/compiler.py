from random import choices
from string import ascii_lowercase, ascii_uppercase
from textwrap import indent
from re import compile as re_compile
import pkgutil

from .extractor import TestcellBlock 

clean_pat = re_compile('\W|^(?=\d)')

import os

# with open("./test_file_template.py.template", "r") as f:
#     test_file_template = f.read()
#
# with open("./test_function_template.py.template", "r") as f:
#     test_function_template = f.read()
#
# with open("./test_code_block_template.py.template", "r") as f:
#     test_code_block_template = f.read()

test_file_template = pkgutil.get_data(__name__, "test_file_template.py.template").decode("utf-8")

test_function_template = pkgutil.get_data(__name__, "test_function_template.py.template").decode("utf-8")

test_code_block_template = pkgutil.get_data(__name__, "test_code_block_template.py.template").decode("utf-8")

def format_testcase_function(
        testcase: str,
        testcase_num: int
    ) -> str:
    testcase_clean = clean_pat.sub("_", testcase)
    return test_function_template.format(test_name=testcase_clean, test_number=testcase_num)
def compile_code_and_tests_into_py(
    code_blocks: TestcellBlock,
    ):
    """Given code and test blocks with testcase names matched by codeblock names, 
    return a python file that is pytest testable.

    Args:
        code_blocks: TestcellBlock containing relevant code.

    Returns:
        A string containing the python code that can be written to a file for pytest testing.
    """

    part_name = choices(ascii_lowercase + ascii_uppercase, k=20)
    part_name = "".join(part_name)

    func_name = choices(ascii_lowercase + ascii_uppercase, k=20)
    func_name = "".join(func_name)
    
    test_code = ""
    for testcase in code_blocks.cases:
        code_content = code_blocks.get_code_for_testcase(testcase)
        test_content = code_blocks.get_test_for_testcase(testcase)
        test_content = indent(test_content, "    ")
        
        test_code += test_code_block_template.format(
            assignment_code = code_content,
            test_code = test_content,
            argument = part_name,
            test_part = testcase.replace('"', '\\"')
        )

    test_code = indent(test_code, "    ")

    testcase_functions = ""
    for i, testcase in enumerate(code_blocks.cases):
        testcase_functions += format_testcase_function(testcase, i)

    return test_file_template.format(
        function_name = func_name,
        argument_name = part_name,
        test_code = test_code,
        test_functions = testcase_functions
    )
