//bibliotecas:
#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

//função main que aceita um comando de linha:
int main(int argc, string argv[])
{
    // verifica se tem somente dois argumentos:
    if (argc != 2)
    {
        //se não printa como usar o programa:
        printf("Usage: ./caesar key\n");
        return 1;
    }
    
    // uma vez que o argv for correto, botar a "key" dentro da variável "key":
    int key = atoi(argv[1]);

    // verifica se o número inteiro é positivo:
    if (key <= 0)
    {
        printf("Usage: ./caesar key (key is a positive value)\n");
        return 1;
    }
    else
    {
        // pede para o usuário um código para encriptar e armazena a respota em "plaintext":
        string plaintext = get_string("plaintext: ");
        //loop:
        printf("ciphertext: ");
        for (int i = 0, n = strlen(plaintext); i < n; i++)
        {
            //verifica se a letra esta maíscula ou minúscula, encripta ela e a escreve:
            if islower(plaintext[i])
            {
                printf("%c", (((plaintext[i] + key) - 97) % 26) + 97);
            }
            else if isupper(plaintext[i])
            {
                printf("%c", (((plaintext[i] + key) - 65) % 26) + 65);
            }
            //se não for nenhum dos dois só escrever ela igual:
            else
            {
                printf("%c", plaintext[i]);
            }   
        }
        printf("\n");
        return 0;
    }
}
