"""
Arquivo de entrada para a aplicação cli.
"""
from sys import argv
from pathlib import Path

from sys import argv
from pathlib import Path

from commands import *

command_map = {
    "train": train,
    "askWithAI": ask_with_ai,
    "ask": ask,
}

def main() -> None:
    global argv

    if "-d" not in argv:
        default_data_dir = Path("./default_data/")

        if not default_data_dir.is_dir():
            print(f"Couldn't load default_data, registered path is not a dir or not even exists.")
        else:
            print(f"--------------Loading default_data--------------")

            docs_list = []
            for doc in default_data_dir.iterdir():
                docs_list.append("@" + str(doc.resolve()))

            train(docs_list)

    print("Entering on personalized command line...")

    while True:
        argv = split_ignoring_while_in_char(input(""))

        if argv[0] == "quit":
            break
        elif command_map.get(argv[0], False):
            command_map[argv[0]](argv[1:])
        else:
            raise Exception(f"Command {argv[0]} not found!!!")

def split_ignoring_while_in_char(
        string: str, 
        sep: str = " ", 
        ignore_while_in: list[str] = ['\"', "\'"],
    ) -> list[str]:
    """
    Separa um string em sep.
    Se um caractere de ignore_while_in 
    aparecer sep será ignorado e tudo que estiver entre 
    este caractere será passado como um item.
    """
    result = [""]

    part_count = 0
    ignore_sep = False
    ignore_sep_with = ""
    for c in string:
        # Checa se o caractere que abriu um espaço para ignorar sep foi fechado e toma as previdências
        if c == ignore_sep_with:
            ignore_sep = toggle_bool(ignore_sep)
            ignore_sep_with = ""
        elif ignore_sep:
            result[part_count] += c
        # Checa se um espaço onde sep é ignorado deve ser aberto e abre.
        elif c in ignore_while_in:
            ignore_sep = toggle_bool(ignore_sep)
            ignore_sep_with = c
        elif c != sep:
            result[part_count] += c
        else:
            result.append("")
            part_count += 1

    return result

def toggle_bool(b: bool) -> bool:
    if b:
        return False
    
    return True


if __name__ == "__main__":
    main()