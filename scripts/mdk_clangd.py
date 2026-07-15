from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[1]
    print("TODO: generate compile_commands.json from MDK project")
    print(f"root: {root}")


if __name__ == "__main__":
    main()
