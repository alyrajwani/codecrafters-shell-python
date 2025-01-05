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
        match command:
            case "exit": 
                handle_exit(command, args)
            case "echo":
                handle_echo(command, args)
            case "type":
                handle_type(command, args)
            case _:
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

def handle_type(command, args):
    if not args:
        pass
    elif args in VALID_COMMANDS:
        print(f"{args} is a shell builtin")
    else:
        print(f"{args}: not found")

if __name__ == "__main__":
    main()
