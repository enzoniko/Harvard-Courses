# Importa função "get_int" da biblioteca cs50
from cs50 import get_int
# Pede a altura da pirâmide
height = get_int("How tall is the Pyramid? ")
# Enquanto não for um valor entre 1 e 8 inclusive, repete a pergunta
while height < 1 or height > 8:
    height = get_int("How tall is the Pyramid? ")
# Pega o valor da altura e divide em andares
for i in range(height):
    # Escreve os espaços necessários
    for j in range(height - i - 1):
        print(" ", end="")
    # Escreve os blocos necessários
    for j in range(i + 1):
        print("#", end="")
    # Divide os andares
    print()