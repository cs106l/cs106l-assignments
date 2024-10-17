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
          bin_dir = os.path.join(venv_path, "Scripts")
        else: 
          bin_dir = os.path.join(venv_path, "bin")

        env = os.environ.copy()
        env["PATH"] = os.pathsep.join([bin_dir, *env.get("PATH", "").split(os.pathsep)])
        env["VIRTUAL_ENV"] = venv_path  # virtual env is right above bin directory
        env["VIRTUAL_ENV_PROMPT"] = os.path.basename(venv_path)
        
        interpreter_path = os.path.join(bin_dir, "python")
        result = subprocess.run([interpreter_path] + sys.argv, env=env)
        sys.exit(result.returncode)

check_virtualenv()

def install_requirements():
    import sys
    import subprocess
    import os

    # pip might need to be updated for packages to install, so let's make sure
    def check_pip_update():
      result = subprocess.run([sys.executable, "-m", "pip", "list", "--outdated"],
                              stdout=subprocess.PIPE, text=True)
      return "pip" in result.stdout 
    
    if check_pip_update():
      print("⏳ Detected outdated pip version. Updating...")
      subprocess.check_call(
          [sys.executable, "-m", "pip", "install", "-U", "pip"],
          stdout=subprocess.DEVNULL,
      )

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
    parts: List[TestPart] = []
    setup: Optional[Callable[[], None]] = None
    teardown: Optional[Callable[[], None]] = None

    def __init__(self):
        self.parts = []

    def add_part(self, name: str, func: Callable[[], bool]) -> None:
        self.parts.append(TestPart(name, func))

    def run(self) -> None:
        if not self._run_lifecycle("set up", self.setup):
            return

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

        if not self._run_lifecycle("tear down", self.teardown):
            return

        if not failures:
            message = "🚀🚀🚀 Congratulations, your code passed all the autograder tests! 🚀🚀🚀"
            message = message.ljust(75)
            print(
                f"\n{Back.LIGHTGREEN_EX}{Fore.LIGHTWHITE_EX}{message}{Style.RESET_ALL}"
            )

    def _run_lifecycle(self, label: str, func: Optional[Callable[[], None]]) -> bool:
        if func is None: return True
        try:
            func()
        except Exception as e:
            print(f"{Fore.RED}❌ Failed to {label} autograder {Fore.RESET}")
            print(f"{Style.BRIGHT}Error:{Style.DIM} {e}{Style.RESET_ALL}")
            return False
        return True
      
