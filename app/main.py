import sys

def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        user_input = input()
        [command, args] = user_input.split(" ", 1)

        match command:
            case "exit": 
                sys.exit(args)
            case "echo":
                print(f"{args}")
            case _:
                print(f"{command} {args}: command not found")

if __name__ == "__main__":
    main()
