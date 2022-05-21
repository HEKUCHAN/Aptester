import os
import sys
import psutil
import subprocess
from time import sleep
from typing import ByteString, Optional, List


class Process:
    def __init__(
        self,
        command: str,
        executable: str,
        input: Optional[str] = None
    ) -> None:
        self.command: List[bytes] = command.split()
        self.input: Optional[str] = input
        self.executable: str = executable

        if self.input is not None:
            self.input = input.encode('utf-8')

    def run(self):
        process = subprocess.Popen(
            self.command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        max_memory = 0

        print(self.command, process.pid)

        while process.wait() is None:
            try:
                usage_memory = psutil.Process(process.pid).memory_info().rss / 1024

                if usage_memory > max_memory:
                    max_memory = usage_memory
            except:
                pass
        else:
            process_stdout = process.stdout.read().decode()
            process_error = process.stderr.read().decode()

        print(process_stdout.split("\n")[-2])
        print(process.pid, max_memory, "END")


Process(
    'python test.py',
    executable=sys.executable
).run()