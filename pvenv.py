import os
import subprocess
import sys
import argparse


def create_virtual_env(env_name, requirements, python_version=None):
    # Create virtual environment
    if python_version:
        subprocess.check_call(
            [sys.executable, '-m', 'venv', '--prompt', env_name, '--python', python_version])
    else:
        subprocess.check_call([sys.executable, '-m', 'venv', env_name])
    print(f"Virtual environment '{env_name}' created.")

    # Activate virtual environment
    activate_script = os.path.join(
        env_name, 'Scripts', 'activate') if os.name == 'nt' else os.path.join(env_name, 'bin', 'activate')
    print(f"To activate the virtual environment, run: source {
          activate_script}")

    # Upgrade pip
    python_executable = os.path.join(
        env_name, 'Scripts', 'python') if os.name == 'nt' else os.path.join(env_name, 'bin', 'python')
    subprocess.check_call(
        [python_executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
    print("Pip has been upgraded.")

    # Install requirements
    if requirements:
        subprocess.check_call(
            [python_executable, '-m', 'pip', 'install', '-r', requirements])
        print("Requirements have been installed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Create a virtual environment.')
    parser.add_argument('env_name', type=str,
                        help='The name of the virtual environment.')
    parser.add_argument('requirements', type=str, nargs='?',
                        help='The requirements file for the virtual environment.')
    parser.add_argument(
        '--python', type=str, help='The Python version to use for the virtual environment.')

    args = parser.parse_args()
    create_virtual_env(args.env_name, args.requirements, args.python)
