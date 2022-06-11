import sys
from typing import Optional, Union, List, Any

from Aptester.judgment import TestCase

class Tester:
    def __init__(
        self,
        command: str,
        test_cases: List[TestCase],
        threading: bool = False,
        limit_memory: int = 1024,
        timeout_ms: Union[int, float]= 60000
    ):
        def __init__(self):
            self.command = command
            self.threading = threading
            self.test_cases = test_cases
            self.timeout_ms = timeout_ms
            self.limit_memory = limit_memory

        