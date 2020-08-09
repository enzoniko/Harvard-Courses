# Importa função "get_float" da biblioteca cs50
from cs50 import get_float
# Variáveis
m = 0
atual = 25
# Enquanto o valor não for positivo, repete a pergunta
while True:
    valor = get_float("Change Owed? ")
    apagar = round(valor * 100)
    if valor > 0:
        break
# Enquanto o valor for positivo, faz os loops
while (valor > 0):
    if (atual <= apagar):
        apagar -= atual
        m += 1
    else:
        if (apagar == 0):
            break
        elif (atual == 25):
            atual = 10
        elif (atual == 10):
            atual = 5
        elif (atual == 5):
            atual = 1
# Printa a quantidade mínima de moedas
print(m)