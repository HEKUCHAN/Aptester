import psutil
import threading
import subprocess
from typing import Optional, Union, List


class Task(threading.Thread):
    def __init__(
        self,
        command: str,
        executable: str,
        input: Optional[str] = None,
        timeout_ms: Optional[int] = None
    ) -> None:
        threading.Thread.__init__(self)

        self.timeout = timeout_ms
        self.executable: str = executable
        self.command: List[str] = command.split()
        self.input: Union[str, bytes, None] = input

        if self.input is not None:
            self.input = input.encode('utf-8')

        if self.timeout is not None:
            self.timeout /= 1000

        # initial variables
        self.pid: int = 0
        self.max_memory_kb: int = 0
        self.process = subprocess.Popen(
            self.command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        self.pid: int = self.process.pid
        self.is_timeout: bool = False

        self.stdout: Optional[str] = None
        self.error: Optional[str] = None

    def communicate(self) -> None:
        try:
            self.stdout, self.error = self.process.communicate(
                self.input,
                timeout=self.timeout
            )
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.is_timeout = True

            return

        self.stdout: Optional[str] = self.stdout.decode()
        self.error: Optional[str] = self.error.decode()

    def check_memory(self) -> None:
        while True:
            try:
                process_info: psutil.Process = psutil.Process(self.pid)
                usage_memory_kb: float = process_info.memory_info().rss / 1024
            except:
                break

            if usage_memory_kb > self.max_memory_kb:
                self.max_memory_kb = usage_memory_kb

    def run(self) -> None:
        memory_observer = threading.Thread(target=self.check_memory)
        process_observer = threading.Thread(target=self.communicate)

        process_observer.start()
        memory_observer.start()

        process_observer.join()
        memory_observer.join()

if __name__ == "__main__":
    import sys

    task = Task(
        'python test.py',
        executable=sys.executable
    )

    task.run()

    print(task.stdout, task.max_memory_kb, end="")
