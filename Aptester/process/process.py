import sys
import psutil
import threading
import subprocess
from typing import Optional, Union, List


class Process(threading.Thread):
    def __init__(
        self,
        command: str,
        executable: str,
        input: Optional[str] = None
    ) -> None:
        threading.Thread.__init__(self)

        self.executable: str = executable
        self.command: List[str] = command.split()
        self.input: Union[str, bytes, None] = input

        if self.input is not None:
            self.input = input.encode('utf-8')

        # initial variables
        self.pid: int = 0
        self.max_memory: int = 0
        self.process = subprocess.Popen(
            self.command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        self.pid = self.process.pid

        self.process_stdout: Optional[str] = None
        self.process_error: Optional[str] = None

    def check_memory(self, pid) -> None:
        while True:
            try:
                process_info: psutil.Process = psutil.Process(pid)
                usage_memory: float = process_info.memory_info().rss / 1024
            except:
                break

            if usage_memory > self.max_memory:
                self.max_memory = usage_memory

    def communicate(self, process, input) -> None:
        self.process_stdout, self.process_error = process.communicate(input)

        self.process_stdout: Optional[str] = self.process_stdout.decode()
        self.process_error: Optional[str] = self.process_error.decode()

    def run(self):
        memory_observer = threading.Thread(target=self.check_memory, args=(self.pid, ))
        process_observer = threading.Thread(target=self.communicate, args=(self.process, self.input, ))

        process_observer.start()
        memory_observer.start()

        process_observer.join()
        memory_observer.join()
