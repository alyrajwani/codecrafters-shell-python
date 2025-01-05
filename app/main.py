import sys

def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        command = input()
        
        match command:
            case "exit 0": 
                break
            case _:
                print(f"{command}: command not found")

if __name__ == "__main__":
    main()
