import os
import subprocess
import sys

def locate_executable(command):
    paths = os.getenv("PATH").split(":")
    for path in paths:
        file_path = os.path.join(path, command)
        if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
            return file_path
    return None

def handle_exit(args):
    sys.exit(int(args[0]) if args else 0)

def handle_echo(args):
    echoed = " ".join(args)
    if (echoed[0] == '"' and echoed[-1] == '"') or (echoed[0] == "'" and echoed[-1] == "'"):
        echoed = echoed[1:-1]
    print(echoed)

def handle_type(args):
    if args[0] in VALID_COMMAND_DICT:
        print(f"{args[0]} is a shell builtin")
    elif executable := locate_executable(args[0]):
        print(f"{args[0]} is {executable}")
    else:
        print(f"{args[0]} not found")

def handle_pwd(args):
    print(f"{os.getcwd()}")

def handle_cd(args):
    path = "".join(args)
    try:
        os.chdir(os.path.expanduser(f"{path}"))
    except OSError:
        print(f"cd: {path}: No such file or directory")

VALID_COMMAND_DICT = {
        "exit"  : handle_exit,
        "echo"  : handle_echo,
        "type"  : handle_type,
        "pwd"   : handle_pwd,
        "cd"    : handle_cd,
        }

def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        command, *args = input().split(" ")
        if command in VALID_COMMAND_DICT:
            VALID_COMMAND_DICT[command](args)
            continue
        elif executable := locate_executable(command):
            subprocess.run([executable, *args])
        else:
            print(f"{command}: command not found")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
