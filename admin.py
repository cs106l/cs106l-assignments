import subprocess
import shutil
import os
import argparse


def find_last_commit_with_path(path):
    try:
        commit_hash = subprocess.check_output(
            ["git", "log", "-n", "1", "--pretty=format:%H", "--", path],
            stderr=subprocess.DEVNULL
        ).decode("utf-8").strip()
        return commit_hash
    except subprocess.CalledProcessError:
        return None

def copy_from_commit(commit_hash, path):
    os.makedirs(path, exist_ok=True)
    subprocess.run(["git", "checkout", commit_hash, "--", path])
    shutil.copytree(path, path, dirs_exist_ok=True)


def main():
    parser = argparse.ArgumentParser(description="Copies an old assignment into the worktree.")
    parser.add_argument("assignment", help="An assignment, e.g. 'assign0', 'assign1', etc.")
    args = parser.parse_args()

    path = args.assignment
    commit_hash = find_last_commit_with_path(path)

    if commit_hash:
        print(f"Last commit for {path}: {commit_hash}")
        copy_from_commit(commit_hash, path)
        print(f"Copied {path} from commit {commit_hash}.")
    else:
        print(f"No commits found for the specified assignment: {path}.")

main()