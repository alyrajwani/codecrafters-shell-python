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

def handle_echo(args, output_file=None):
    output = " ".join(args)
    if output_file:
        with open(output_file, 'w') as file:
            file.write(output + "\n")
    else:
        print(output)

def handle_type(args, output_file=None):
    result = ""
    if args[0] in VALID_COMMAND_DICT:
        result = f"{args[0]} is a shell builtin"
    elif executable := locate_executable(args[0]):
        result = f"{args[0]} is {executable}"
    else:
        result = f"{args[0]} not found"
    if output_file:
        with open(output_file, 'w') as file:
            file.write(result + "\n")
    else:
        print(result)

def handle_pwd(args, output_file=None):
    output = os.getcwd()
    if output_file:
        with open(output_file, 'w') as file:
            file.write(output + "\n")
    else:
        print(output)

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

def parse_redirection(command_parts):
    if '>' in command_parts:
        redirection_index = command_parts.index('>')
        if redirection_index == len(command_parts) - 1:
            raise ValueError("Syntax error: unexpected end of file")
        output_file = command_parts[redirection_index + 1]
        command_parts = command_parts[:redirection_index]
        return command_parts, output_file
    return command_parts, None

def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        try:
            user_input = input()
            if not user_input.strip():
                continue

            command_parts, output_file = parse_redirection(shlex.split(user_input))
            if not command_parts:
                continue

            command = command_parts[0]
            args = command_parts[1:]

            if command in VALID_COMMAND_DICT:
                VALID_COMMAND_DICT[command](args, output_file)
            elif executable := locate_executable(command):
                with open(output_file, 'w') if output_file else sys.stdout as out:
                    subprocess.run([executable] + args, stdout=out, stderr=sys.stderr)
            else:
                message = f"{command}: command not found"
                if output_file:
                    with open(output_file, 'w') as file:
                        file.write(message + "\n")
                else:
                    print(message)
        except EOFError:
            break
        except ValueError as e:
            print(e)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()

