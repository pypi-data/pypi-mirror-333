from argparse import ArgumentParser
from colorama import Fore, init
from template_tool.colorization import color
from template_tool import (
    args_desc,
)
from template_tool.actions import (
    load,
    save,
    list,
    remove
)

init(convert=True)


def main():
    parser = ArgumentParser(description="a template tool")

    parser.add_argument(
        "-l",
        "--load",
        type=str,
        help="--load <template-name>"
    )

    parser.add_argument(
        "-s",
        "--save",
        type=str,
        help="--save <template-name>"
    )

    parser.add_argument(
        "--list",
        action="store_true",
        help="--list"
    )

    parser.add_argument(
        "--remove",
        type=str,
        help="--remove <template-name>"
    )

    args = parser.parse_args()

    if args.load:
        load.load(args.load)
    elif args.save:
        save.save(args.save)
    elif args.list:
        list.list()
    elif args.remove:
        remove.remove(args.remove)
    else:
        for arg, desc in args_desc.items():
            print(f"\"{color(Fore.GREEN, arg)}\": \"{color(Fore.YELLOW, desc)}\"")


if __name__ == "__main__":
    main()
