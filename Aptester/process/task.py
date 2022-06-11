import psutil
import threading
import subprocess
from typing import Optional, Union, List


class Task(threading.Thread):
    """Task class
    This class used for create process task.
    You can runs the task using run method.

    Attributes:
        command (str) : Parameter to set that command you would like to execute.
        input: (str) : Parameter to set the standard input of your process.
        timeout_ms: (int, float) : parameter to set timeout. Defaults to None.
            if a TimeOutError detected, the is_timeout property is set to True.
            Defaults to None(No timeout).

    Todo:
        * Add counter of process time
    """
    def __init__(
        self,
        command: str,
        input: Optional[str] = None,
        timeout_ms: Optional[Union[int, float]] = None
    ) -> None:
        # Instancing super class
        threading.Thread.__init__(self)

        self.timeout = timeout_ms
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

    def run(self) -> None:
        """Task.run
        This method used to run the process observers and memory observers.
        It also stores the process info in stdout, stderr, max_memory_kb properties
        at the end of the process.

        And when _communicate method execute, in same time _check_memory method execute.
        """

        memory_observer = threading.Thread(target=self._check_memory)
        process_observer = threading.Thread(target=self._communicate)

        process_observer.start()
        memory_observer.start()

        process_observer.join()
        memory_observer.join()

    def _communicate(self) -> None:
        """Task._communicate
        This method initiates execution of the command.
        if a TimeOutError detected, the is_timeout property is set to True.
        """

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

    def _check_memory(self) -> None:
        """Task._check_memory
        This method checks memory usage during main process execution.
        It also stores the maximum memory usage in the max_memory_kb property
        at the end of the process.

        Note:
            * DO NOT EXECUTE BEFORE _communicate class method.
              if this class method executed before _communicate method,
              the method process just break.
        """

        while True:
            try:
                process_info: psutil.Process = psutil.Process(self.pid)
                usage_memory_kb: float = process_info.memory_info().rss / 1024
            except:
                break

            if usage_memory_kb > self.max_memory_kb:
                self.max_memory_kb = usage_memory_kb

if __name__ == "__main__":
    task = Task(
        'python test.py',
    )

    task.run()

    print(task.stdout, task.max_memory_kb, end="")
