# BIBLIOTECAS
from cs50 import get_int, get_string
from sys import argv, exit
# VERIFICA OS ARGUMENTOS
if (len(argv) != 2):
    print("Usage: python caesar.py key")
    exit(1)
# ARMAZENA CERTINHO
key = int(argv[1])
# VERIFICA SE É POSITIVO
if (key <= 0):
    print("Usage: ./caesar key (key is a positive value)")
    exit(1)
# LOOP
else:
    plaintext = get_string("plaintext: ")
    print("ciphertext: ", end="")
    for i in plaintext:
        if (i.islower()):
            print(chr((((ord(i) + key) - 97) % 26) + 97), end="")
        elif (i.isupper()):
            print(chr((((ord(i) + key) - 65) % 26) + 65), end="")
        else:
            print(i, end="")
    print()
    # SUCESSO
    exit(0)