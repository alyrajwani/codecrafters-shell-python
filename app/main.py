import os
import shlex
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
    for i in range(len(args)):
        if (args[i].startswith("'") and args[i].endswith("'")) or (
            args[i].startswith('"') and args[i].endswith('"')
        ):
            args[i] = args[i][1:-1]  # Remove surrounding quotes
    return " ".join(args)

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
    "exit": handle_exit,
    "echo": handle_echo,
    "type": handle_type,
    "pwd": handle_pwd,
    "cd": handle_cd,
}

def parse_redirection(args):
    output_file = None
    error_file = None
    append = False
    error_append = False

    if ">>" in args or "1>>" in args:
        idx = args.index(">>") if ">>" in args else args.index("1>>")
        output_file = args[idx + 1]
        args = args[:idx]
        append = True
    elif ">" in args or "1>" in args:
        idx = args.index(">") if ">" in args else args.index("1>")
        output_file = args[idx + 1]
        args = args[:idx]

    if "2>>" in args:
        idx = args.index("2>>")
        error_file = args[idx + 1]
        args = args[:idx]
        error_append = True
    elif "2>" in args:
        idx = args.index("2>")
        error_file = args[idx + 1]
        args = args[:idx]

    return args, output_file, error_file, append, error_append

def execute_command(command, args):
    args, output_file, error_file, append, error_append = parse_redirection(args)
    stdout = None
    stderr = None

    if output_file:
        mode = "a" if append else "w"
        stdout = open(output_file, mode)

    if error_file:
        mode = "a" if error_append else "w"
        stderr = open(error_file, mode)

    try:
        if command in VALID_COMMAND_DICT:
            result = VALID_COMMAND_DICT[command](args)
            if result:
                if stdout:
                    stdout.write(result + "\n")
                else:
                    print(result)
        elif executable := locate_executable(command):
            subprocess.run([executable, *args], stdout=stdout, stderr=stderr)
        else:
            print(f"{command}: command not found")
    finally:
        if stdout:
            stdout.close()
        if stderr:
            stderr.close()

def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        command, *args = shlex.split(input())
        execute_command(command, args)
        sys.stdout.flush()

if __name__ == "__main__":
    main()
