import os
import sys

VALID_COMMANDS = ["exit", "echo", "type"]

def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        user_input = input()
        command = user_input.split(" ", 1)[0]
        args = None
        if len(user_input.split(" ", 1)) == 2:
            args = user_input.split(" ", 1)[1]
        paths = os.getenv("PATH").split(":")

        match command:
            case "exit": 
                handle_exit(command, args)
            case "echo":
                handle_echo(command, args)
            case "type":
                handle_type(command, args, paths)
            case _:
                if os.path.isfile(command):
                    os.system(command)
                else:
                    print(f"{command}: command not found")

def handle_echo(command, args):
    if not args:
        pass
    else:
        print(f"{args}")

def handle_exit(command, args):
    if not args:
        pass
    else:
        exit(int(args))

def handle_type(command, args, paths):
    if not args:
        pass
    elif args in VALID_COMMANDS:
        print(f"{args} is a shell builtin")
    else: 
        arg_path = None
        for path in paths:
            if os.path.isfile(f"{path}/{args}"):
                arg_path = f"{path}/{args}"
        if arg_path:
            print(f"{args} is {arg_path}")
        else:
            print(f"{args}: not found")

if __name__ == "__main__":
    main()
