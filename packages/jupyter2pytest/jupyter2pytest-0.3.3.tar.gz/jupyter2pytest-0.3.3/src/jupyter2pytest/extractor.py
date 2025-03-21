from typing import List, Dict
from collections import defaultdict
from re import compile

import nbformat

class TestcellBlock:
    """Class for associating testcases with code blocks.

    Attributes: 
        cases: List of all cases in notebook file (i.e. list of 'things' extracted)
        code_blocks: Association of cases with code blocks corresponding to them.
        test_blocks: Association of cases with test code blocks corresponding to them.
        temp_code_blocks: List of code blocks that have not yet been associated with a testcase.
    """
    cases: List[str]
    code_blocks: Dict[str, List[str]]
    test_blocks: Dict[str, List[str]]
    temp_code_blocks: List[str]

    def __init__(
            self
        ) -> None:
        self.cases = []
        self.code_blocks = defaultdict(lambda: [])
        self.temp_code_blocks = []
        self.test_blocks = defaultdict(lambda: [])

    def add_codeblock(
            self, 
            code: str
        ) -> None:
        """Adds a block of code corresponding to a testcase. This will be added
            to the next testcase that is added.

        Args:
            code: The code block to add.
        """
        
        self.temp_code_blocks.append(code)

    def add_testblock(
        self,
        testcase: str,
        code: str
        ) -> None:

        """Adds a block of code corresponding to a testcase.

        Args:
            testcase: The name of the testcase to add.
            code: The code corresponding to the testcase.
        """
        self.test_blocks[testcase].append(code)

        if len(self.temp_code_blocks) > 0:
            self.code_blocks[testcase] = self.temp_code_blocks

        self.temp_code_blocks = []

        if testcase not in self.cases:
            self.cases.append(testcase)

    def get_code_for_testcase(
            self,
            testcase: str
        ) -> str:
        """Gets all code corresponding to a given testcase.

        Args:
            testcase: The testcase to get code for.

        Returns:
            All blocks of code corresponding to the testcase, joined by newlines.
        """
        if testcase in self.cases:
            return "\n".join(self.code_blocks[testcase])
        else:
            return ""

    def get_test_for_testcase(
        self,
        testcase: str
        ) -> str:
        """Gets all test code corresponding to a given testcase.

        Args:
            testcase: The testcase to get code for.

        Returns:
            All blocks of code corresponding to the testcase, joined by newlines.
        """
        if testcase in self.cases:
            return "\n".join(self.test_blocks[testcase])
        else:
            return ""

def open_notebook(
        path: str    
    ) -> nbformat.NotebookNode:
    """Opens a python notebook at a given path as a NotebookNode object.

    Args:
        path: Path to the ipynb file.

    Returns:
        NotebookNode object representing the notebook.
    """
    with open(path, "r") as nfp:
        notebook = nbformat.read(nfp, as_version=4)
    return notebook

def extract_with_prefix(
        notebook: nbformat.NotebookNode,
        prefix: str
    ) -> TestcellBlock:
    """Extract code blocks from a notebook matching a given prefix.
        Note: Code blocks are generated as those blocks that do not match the prefix and
        occur before the testcase has been defined.

    Args:
        notebook: Notebook to extract code blocks from.
        prefix: Regex prefix to both decide if a block is extaction worthy, and to extract the testcase name.
                E.g. "### TEST CASE for Puzzle (.*) ==" 

    Returns:
        TestcellBlock object associating testcase names with code blocks.
    """
    per_testcase_code = TestcellBlock()
    pat = compile(prefix)

    for cell in notebook.cells:
        if cell.cell_type == "code":
            source = cell.source
            newline_idx = source.find("\n")
            first_line = source[:newline_idx]
            rest = source[newline_idx+1:]
            re_match = pat.fullmatch(first_line)
            if re_match is not None:
                testcase_name = re_match.group(1)
                per_testcase_code.add_testblock(testcase_name, rest)
            else:
                per_testcase_code.add_codeblock(source)
    
    return per_testcase_code

