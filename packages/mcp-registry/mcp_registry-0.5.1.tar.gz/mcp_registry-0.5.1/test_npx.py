import os
import shutil
import subprocess


def debug_npx():
    # Print current environment info
    print("=== Environment Information ===")
    print(f"Current PATH: {os.environ.get('PATH')}")
    print(f"Current Shell: {os.environ.get('SHELL')}")
    print(f"Current Working Directory: {os.getcwd()}")

    # Try to find npx using different methods
    print("\n=== Command Location ===")
    try:
        npx_path = shutil.which("npx")
        print(f"shutil.which('npx'): {npx_path}")
    except Exception as e:
        print(f"Error with shutil.which: {e}")

    # Try using shell to find npx
    try:
        shell = os.environ.get("SHELL", "/bin/sh")
        result = subprocess.run([shell, "-c", "which npx"], capture_output=True, text=True)
        print(f"Shell which npx: {result.stdout.strip()}")
        if result.stderr:
            print(f"Shell stderr: {result.stderr}")
    except Exception as e:
        print(f"Error with shell which: {e}")

    # Try running npx directly
    print("\n=== Direct npx execution ===")
    try:
        result = subprocess.run(["npx", "--version"], capture_output=True, text=True)
        print(f"Direct npx output: {result.stdout}")
        print(f"Direct npx stderr: {result.stderr}")
    except Exception as e:
        print(f"Error running npx directly: {e}")

    # Try running npx through shell
    print("\n=== Shell npx execution ===")
    try:
        result = subprocess.run(
            [shell, "-c", "npx --version"], capture_output=True, text=True, env=os.environ
        )  # Explicitly pass current environment
        print(f"Shell npx output: {result.stdout}")
        print(f"Shell npx stderr: {result.stderr}")
    except Exception as e:
        print(f"Error running npx through shell: {e}")


if __name__ == "__main__":
    debug_npx()
