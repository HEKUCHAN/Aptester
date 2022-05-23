import os
import sys
import psutil
import subprocess
from time import sleep
from typing import Optional, List


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

        while process.poll() is None:
            try:
                process_info = psutil.Process(process.pid)
                usage_memory = process_info.memory_info().rss / 1024

                print(process_info.status())
            except:
                break

            if usage_memory > max_memory:
                max_memory = usage_memory

        process_stdout, process_error = process.communicate(self.input)

        print(process_stdout.decode(

        ).split("\n")[-2])
        print(process.pid, max_memory, "Kb", "END")


Process(
    'python test.py',
    executable=sys.executable
).run()