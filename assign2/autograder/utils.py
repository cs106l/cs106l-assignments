def check_virtualenv():
    import sys
    import os
    import subprocess

    if not hasattr(sys, 'real_prefix') and (sys.base_prefix == sys.prefix):
        print("🔍 Not in a virtual environment. Creating one in 'autograder/'...")
        venv_path = os.path.dirname(os.path.abspath(__file__))
        subprocess.check_call([sys.executable, '-m', 'venv', venv_path])
        print("✅ Virtual environment created.")

        if os.name == "nt":
          interpreter_path = os.path.join(venv_path, "Scripts", "python")
        else: 
          interpreter_path = os.path.join(venv_path, "bin", "python")
        result = subprocess.run([interpreter_path] + sys.argv)
        sys.exit(result.returncode)

check_virtualenv()

def install_requirements():
    import sys
    import subprocess
    import os

    REQUIREMENTS = os.path.join(os.path.dirname(__file__), "requirements.txt")
    print("⏳ Installing autograder packages (this may take a few minutes)...")
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "-r", REQUIREMENTS],
        stdout=subprocess.DEVNULL,
    )
    print("✅ Autograder packages installed.")


# Install autograder packages on import
install_requirements()

from dataclasses import dataclass
from typing import Callable, List, Optional, Union
from colorama import Fore, init, Style, Back

init()

@dataclass(frozen=True)
class TestPart:
    name: str
    func: Callable[[], Union[bool, None]]


class Autograder:
    parts: List[TestPart]
    setup: Optional[Callable[[], None]]
    teardown: Optional[Callable[[], None]]

    def __init__(self):
        self.parts = []

    def add_part(self, name: str, func: Callable[[], bool]) -> None:
        self.parts.append(TestPart(name, func))

    def run(self) -> None:
        if self.setup:
            self.setup()

        failures = False
        for part in self.parts:
            header = f"Running test: {part.name}... 🧪".ljust(80)
            print(f"\n{Back.CYAN}{Fore.LIGHTWHITE_EX}{header}{Style.RESET_ALL}")

            result = None
            error = None

            try:
                result = part.func()
            except Exception as e:
                error = e
                result = False

            if result is None or result:
                print(f"{Fore.GREEN}✅ {part.name} passed! 🚀 {Fore.RESET}")
            else:
                print(f"{Fore.RED}❌ {part.name} failed! 😞 {Fore.RESET}")
                if error:
                    print(f"{Style.BRIGHT}Error:{Style.DIM} {error}{Style.RESET_ALL}")
                failures = True

        if not failures:
            message = "🚀🚀🚀 Congratulations, your code passed all the autograder tests! 🚀🚀🚀"
            message = message.ljust(75)
            print(
                f"\n{Back.LIGHTGREEN_EX}{Fore.LIGHTWHITE_EX}{message}{Style.RESET_ALL}"
            )

        if self.teardown:
            self.teardown()
