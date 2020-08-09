# BIBLIOTECAS
from cs50 import get_string
from sys import argv

words = set()


def main():

    # VERIFICA O ARGUMENTO
    if len(argv) != 2:
        print("Usage: python bleep.py dictionary")
        exit(1)

    # BAIXA O ARQUIVO DE TEXTO
    load(argv[1])

    # PEDE A MENSAGEM PARA O USUÁRIO
    user_in = get_string("What message would you like to censor? ")
    # DIVIDE EM TOKENS
    tokens = user_in.split()

    # VERIFICA COM O TEXTO
    for i in tokens:
        if check(i):
            for j in i:
                print("*", end="")
        else:
            print(i, end="")
        print(" ", end="")
    print()

    return True


def load(banned):
    # BAIXA AS PALAVRAS NO ARQUIVO DE TEXTO
    file = open(banned, "r")
    for line in file:
        words.add(line.rstrip("\n"))
    file.close()
    return True


def check(word):
    # RETORNA TRUE SE A PALAVRA ESTIVER NO DICIONÁRIO, SENÃO RETORNA FALSE
    return word.lower() in words


if __name__ == "__main__":
    main()