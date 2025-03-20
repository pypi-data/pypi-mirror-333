from colorama import Fore, init

init(convert=True)

def color(color: str, txt: str) -> str:
    return f"{color}{txt}{Fore.RESET}"
