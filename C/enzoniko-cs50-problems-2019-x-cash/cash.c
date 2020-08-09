//Bibliotecas:
#include <cs50.h>
#include <stdio.h>
#include <math.h>
//Função main:
int main(void)
{
    //variáveis:
    float valor = printf("Change Owed? ");
    scanf("%f", &valor);
    int m = 0;
    int atual = 25;
    int apagar = round(valor * 100);
    //verifica se o input é positivo:
    while (valor <= 0)
    {
        printf("Change Owed? ");
        scanf("%f", &valor);
        apagar = round(valor * 100);
    }
    //se for positvo faz as coisas abaixo:
    while (valor > 0)
    {
        //da a quantidade de moedas:
        if (atual <= apagar)
        {
            apagar -= atual;
            m += 1;
        }
        else
        {
            //faz os cálculos diminuindo a quantidade do dinheiro:
            if (apagar == 0)
            {
                break;
            }
                
            else if (atual == 25)
            {
                atual = 10; 
            }
                
            else if (atual == 10)
            {
                atual = 5; 
            }
                
            else if (atual == 5)
            {
                atual = 1;
            }
        } 
    }   
    //print da quantidade de moedas
    printf("%i\n", m); 
}
