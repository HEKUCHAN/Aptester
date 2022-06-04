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

        self.stdout: Optional[str] = None
        self.error: Optional[str] = None

    def check_memory(self) -> None:
        while True:
            try:
                process_info: psutil.Process = psutil.Process(self.pid)
                usage_memory: float = process_info.memory_info().rss / 1024
            except:
                break

            if usage_memory > self.max_memory:
                self.max_memory = usage_memory

    def communicate(self) -> None:
        self.stdout, self.error = self.process.communicate(self.input)

        self.stdout: Optional[str] = self.stdout.decode()
        self.error: Optional[str] = self.error.decode()

    def run(self):
        memory_observer = threading.Thread(target=self.check_memory)
        process_observer = threading.Thread(target=self.communicate)

        process_observer.start()
        memory_observer.start()

        process_observer.join()
        memory_observer.join()
