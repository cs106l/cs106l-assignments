_AUTOGRADER_PACKAGES = [
    # For logging and color output
    "colorama==0.4.6"
]

# ==============================================================================
# Virtual Environment Setup
# ==============================================================================


def _check_virtualenv():
    import sys
    import os
    import subprocess

    venv_path = os.path.dirname(os.path.abspath(__file__))

    # The first condition checks if we are running in the **correct** virtual environment.
    # The second condition checks if we ran this script to set environment variables correctly.
    if os.environ.get("VIRTUAL_ENV", None) != venv_path or "VIRTUAL_ENV_BIN" not in os.environ:
        config_path = os.path.join(venv_path, "pyvenv.cfg")
        if not os.path.isfile(config_path):
            print("🔍 Virtual environment not found. Creating one in 'autograder/'...")
            subprocess.check_call([sys.executable, "-m", "venv", venv_path])
            print("✅ Virtual environment created.")

        bin_dir = next((bd for bd in ["Scripts", "bin"] if os.path.isdir(os.path.join(venv_path, bd))), None)
        if bin_dir is None:
            raise RuntimeError("Couldn't find 'Scripts' or 'bin' directory in virtual environment")
        bin_dir = os.path.join(venv_path, bin_dir)

        env = os.environ.copy()
        env["PATH"] = os.pathsep.join([bin_dir, *env.get("PATH", "").split(os.pathsep)])
        env["VIRTUAL_ENV"] = venv_path  # virtual env is right above bin directory
        env["VIRTUAL_ENV_BIN"] = bin_dir
        env["VIRTUAL_ENV_PROMPT"] = os.path.basename(venv_path)

        # Fixes encoding errors on Windows (specifically when installing packages with pip)
        env["PYTHONIOENCODING"] = "utf-8"

        interpreter_path = os.path.join(bin_dir, "python")
        result = subprocess.run([interpreter_path] + sys.argv, env=env)
        sys.exit(result.returncode)


_check_virtualenv()


# ==============================================================================
# Pip Package Installation
# ==============================================================================

def _install_requirement(package: str):
    import subprocess
    import sys

    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", package],
        stdout=subprocess.DEVNULL,
    )

def _install_requirements():
    import sys
    import subprocess
    import os

    print("⏳ Installing autograder packages (this may take a few minutes)...")

    # pip might need to be updated for packages to install, so let's make sure
    def check_pip_update():
        # Ensure pip is installed
        subprocess.run([sys.executable, "-m", "ensurepip", "--default-pip"], stdout=subprocess.DEVNULL)
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list", "--outdated"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        return "pip" in result.stdout

    if check_pip_update():
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-U", "pip"],
            stdout=subprocess.DEVNULL,
        )

    REQUIREMENTS = os.path.join(os.path.dirname(__file__), "requirements.txt")

    # Packages required by the core autograder
    for package in _AUTOGRADER_PACKAGES:
        _install_requirement(package)

    # Assignment specific packages
    if os.path.isfile(REQUIREMENTS):
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", REQUIREMENTS],
            stdout=subprocess.DEVNULL,
        )

    print("✅ Autograder packages installed.")


# Install autograder packages on import
_install_requirements()

# ==============================================================================
# Imports
# ==============================================================================

import os
from dataclasses import dataclass
from typing import Callable, List, Optional, Union
from colorama import Fore, init, Style, Back

init()


# ==============================================================================
# Checking for Updates
# ==============================================================================


def check_for_updates():
    import subprocess

    def needs_update() -> bool:
        try:
            subprocess.check_call(
                ["git", "rev-parse", "--is-inside-work-tree"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            subprocess.check_call(
                ["git", "fetch", "origin"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            origin_main_commit = subprocess.check_output(
                ["git", "rev-parse", "origin/main"]
            ).strip()
            result = subprocess.run(
                ["git", "merge-base", "--is-ancestor", origin_main_commit, "HEAD"]
            )
            return result.returncode != 0

        except subprocess.CalledProcessError:
            return False

    if needs_update():
        tab = f"{Back.YELLOW} {Back.RESET} "
        print(
            f"\n{tab}It looks like your assignment might be out of date. Try running:"
            f"\n{tab}\n{tab}\tgit pull origin main"
            f"\n{tab}\n{tab}to fetch any updates, and then re-run your code.\n"
        )


check_for_updates()


# ==============================================================================
# Autograder Core
# ==============================================================================

ASSIGNMENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
AUTOGRADER_DIR = os.path.join(ASSIGNMENT_DIR, "autograder")

TestFunction = Callable[[], Union[bool, None]]
"""
A test function takes no parameters.
It returns True or None if the test passes, and False if the test fails.
It can also throw an exception to indicate failure, the details of which will be printed to the console.
"""

@dataclass(frozen=True)
class TestPart:
    name: str
    func: TestFunction
    special: bool = False


class Autograder:
    parts: List[TestPart] = []
    setup: Optional[TestFunction] = None
    teardown: Optional[TestFunction] = None

    def add_part(self, name: str, func: Callable[[], bool]) -> None:
        self.parts.append(TestPart(name, func))

    def run(self) -> None:
        parts = self.parts.copy()
        if self.setup:
            parts.insert(0, TestPart("Autograder Setup", self.setup, True))
        if self.teardown:
            parts.append(TestPart("Autograder Teardown", self.teardown, True))

        failures = False
        for part in parts:
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
                if not part.special:
                    print(f"{Fore.GREEN}✅ {part.name} passed! 🚀 {Fore.RESET}")
            else:
                print(f"{Fore.RED}❌ {part.name} failed! 😞 {Fore.RESET}")
                if error:
                    print(f"{Style.BRIGHT}Reason:{Style.DIM} {error}{Style.RESET_ALL}")
                failures = True

                if part.special:
                    break

        if not failures:
            message = "🚀🚀🚀 Congratulations, your code passed all the autograder tests! 🚀🚀🚀"
            message = message.ljust(75)
            print(
                f"\n{Back.LIGHTGREEN_EX}{Fore.LIGHTWHITE_EX}{message}{Style.RESET_ALL}"
            )


# ==============================================================================
# CastXML Installation
# ==============================================================================

_castxml_installed: bool = False

def install_castxml():
    global _castxml_installed
    _castxml_installed = True

    castxml_install_packages = [
        # For CastXML installation
        "requests==2.32.3",
        # For CastXML installation
        "py-cpuinfo==9.0.0",
        # For inspecting CPP files in code. 3.x is the first that reads the
        # output of CastXML v2026.01.30 (2.x fails to relink its classes).
        "pygccxml==3.0.2"
    ]

    for package in castxml_install_packages:
        _install_requirement(package)

    bin_path = os.environ.get("VIRTUAL_ENV_BIN")
    castxml_dir = os.path.join(bin_path, "castxml")

    castxml_bin_dir = os.path.join(castxml_dir, "bin")
    os.environ["PATH"] = os.pathsep.join(
        [castxml_bin_dir, *os.environ.get("PATH", "").split(os.pathsep)]
    )

    def get_macos_major():
        import platform
        import subprocess

        version = platform.mac_ver()[0]
        # Pythons built against an old SDK report every macOS since 11 as
        # "10.16", so ask the system directly in that case.
        if not version or version.startswith("10.16"):
            try:
                version = subprocess.run(
                    ["sw_vers", "-productVersion"],
                    capture_output=True,
                    text=True,
                    env={**os.environ, "SYSTEM_VERSION_COMPAT": "0"},
                ).stdout.strip()
            except OSError:
                pass
        try:
            return int(version.split(".")[0])
        except ValueError:
            return 0

    def get_platform_file():
        """The CastXMLSuperbuild release and archive to download for this machine."""
        import platform
        import cpuinfo
        import re

        os_name = platform.system().lower()
        arch = platform.machine().lower()

        # CastXML parses with its own bundled Clang, so that Clang has to
        # understand the student's standard library headers. v0.6.5's is too
        # old for current ones: libc++ in the Command Line Tools for Xcode 16.3+
        # calls __builtin_ctzg, and GCC 15's libstdc++ uses bf16 literals and
        # __assume__, so parsing anything that includes <string> fails.
        # v2026.01.30 bundles LLVM 21. Alma Linux 8 is its most portable Linux
        # build (glibc 2.28).
        if os_name == "linux" and arch == "aarch64":
            return "v2026.01.30", "castxml-alma-linux-8-arm-aarch64.tar.gz"
        elif os_name == "linux":
            return "v2026.01.30", "castxml-alma-linux-8-x86_64.tar.gz"
        elif os_name == "darwin":
            # Need to handle running Python under Rosetta on Apple Silicon
            brand = cpuinfo.get_cpu_info()["brand_raw"]
            is_arm = "arm" in arch or re.match(r"Apple M\d+", brand)
            # The v2026.01.30 macOS binaries need macOS 15. Older Macs cannot
            # install the Command Line Tools with the new headers anyway, so
            # they keep v0.6.5, which parses the headers they do have.
            if get_macos_major() >= 15:
                if is_arm:
                    return "v2026.01.30", "castxml-macos-15-arm64.tar.gz"
                return "v2026.01.30", "castxml-macos-15-intel-x86_64.tar.gz"
            if is_arm:
                return "v0.6.5", "castxml-macos-arm.tar.gz"
            return "v0.6.5", "castxml-macosx.tar.gz"
        elif os_name == "windows":
            # The win11 build links the MSVC runtime, as v0.6.5 did. The
            # windows-2022 one links MinGW's libstdc++-6.dll and crashes when an
            # older copy (Git for Windows ships one) comes first on PATH.
            return "v2026.01.30", "castxml-windows-win11-amd64.zip"

        raise RuntimeError(
            f"It looks like you are running on an unknown platform: {os_name}/{arch}. Please make a post on EdStem!"
        )

    castxml_release, castxml_file = get_platform_file()
    castxml_download_url = f"https://github.com/CastXML/CastXMLSuperbuild/releases/download/{castxml_release}/{castxml_file}"

    # Records which download is unpacked in castxml_dir, so a machine that needs
    # a different build gets it instead of keeping the one it already has.
    # Installs from before this file existed are v0.6.5.
    castxml_version_path = os.path.join(castxml_dir, "cs106l-castxml-url.txt")
    if os.path.isdir(castxml_dir):
        try:
            with open(castxml_version_path) as f:
                installed_url = f.read().strip()
        except OSError:
            installed_url = f"https://github.com/CastXML/CastXMLSuperbuild/releases/download/v0.6.5/{castxml_file}"
        if installed_url == castxml_download_url:
            return
        import shutil
        shutil.rmtree(castxml_dir)

    print("⏳ Installing CastXML...")

    import requests
    import zipfile
    import tarfile

    castxml_archive_path = os.path.join(bin_path, castxml_file)

    with requests.get(castxml_download_url, stream=True) as r:
        r.raise_for_status()
        with open(castxml_archive_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    if castxml_file.endswith(".zip"):
        with zipfile.ZipFile(castxml_archive_path, "r") as zip_ref:
            zip_ref.extractall(bin_path)
    elif castxml_file.endswith(".tar.gz"):
        with tarfile.open(castxml_archive_path, "r:gz") as tar_ref:
            tar_ref.extractall(bin_path)

    with open(castxml_version_path, "w") as f:
        f.write(castxml_download_url)

    print("✅ Installed CastXML!")


def get_declarations(*files: os.PathLike):
    if not _castxml_installed:
        raise RuntimeError(
            "CastXML is not installed. Please run `install_castxml()` before calling `get_declarations()`."
        )

    import subprocess
    from pygccxml import utils as gccutils
    from pygccxml import declarations
    from pygccxml import parser
    import logging

    # This should prevent pygccxml from outputting INFO messages
    gccutils.loggers.set_level(logging.WARNING)

    for file in files:
        abs_path = os.path.join(ASSIGNMENT_DIR, file)
        if not os.path.isfile(abs_path):
            raise FileNotFoundError(f"Couldn't find file: {abs_path}")

    # Grab the C++ parser
    generator_path, generator_name = gccutils.find_xml_generator()

    compiler_path = None
    if os.name == "nt":
        result = result = subprocess.run(
            ["where", "g++"], capture_output=True, text=True
        )
        if result.returncode != 0:
            raise RuntimeError(
                "Couldn't find the path to g++. Did you follow the setup instructions?\n\nhttps://github.com/cs106l/cs106l-assignments"
            )
        compiler_path = result.stdout.strip()
        compiler_path = f'"(" "{compiler_path}" -std=c++11 ")"'

    # Configure the C++ parser
    xml_generator_config = parser.xml_generator_configuration_t(
        xml_generator_path=generator_path,
        xml_generator=generator_name,
        compiler="g++",
        compiler_path=compiler_path,
        working_directory=ASSIGNMENT_DIR,
        ccflags="-std=c++11",
    )

    try:
        decls: List[declarations.declaration_t] = parser.parse(files, xml_generator_config)
    except Exception as e:
        print()
        print(e)
        print()
        print(
            f"{Fore.RED}{Back.YELLOW}Failed to parse {', '.join(files)}. Did you remember to recompile your code?{Style.RESET_ALL}"
        )
        print(
            f"{Fore.LIGHTWHITE_EX}If your code is compiling correctly, please reach out on Ed with the error message above.{Fore.RESET}\n"
        )
        raise Exception("Failed to parse C++ file")
    
    return decls