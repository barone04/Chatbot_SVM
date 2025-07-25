#!/usr/bin/env python
import sys
import warnings

from agent import SQLDeveloperCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'query': 'lấy cho tôi 5 sản phấm giá trên 10000'
    }
    SQLDeveloperCrew().crew().kickoff(inputs=inputs)

run()