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
            args[i] = args[i][1:-1]  
    print(" ".join(args))
    
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

def execute_command_with_redirection(command_parts):
    if '>' in command_parts:
        redirection_index = command_parts.index('>')
        if redirection_index == len(command_parts) - 1:
            print("Syntax error: unexpected end of file")
            return

        file_name = command_parts[redirection_index + 1]
        command = command_parts[:redirection_index]
        with open(file_name, 'w') as file:
            result = subprocess.run(command, stdout=file, stderr=sys.stderr)
            return result.returncode
    else:
        return subprocess.run(command_parts).returncode

def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        try:
            user_input = input()
            if not user_input.strip():
                continue

            command_parts = shlex.split(user_input)
            command = command_parts[0]
            args = command_parts[1:]

            if command in VALID_COMMAND_DICT:
                VALID_COMMAND_DICT[command](args)
            elif executable := locate_executable(command):
                execute_command_with_redirection([executable] + args)
            else:
                print(f"{command}: command not found")
        except EOFError:
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
