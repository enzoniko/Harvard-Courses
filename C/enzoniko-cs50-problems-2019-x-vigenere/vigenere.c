//bibliotecas:
#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

//função main que aceita um comando de linha:
int main(int argc, string argv[])
{
    // verifica se tem argumentos:
    if (argc != 2)
    {
        //se não printa como usar o programa:
        printf("Usage: ./vigenere keyword\n");
        return 1;
    }
    //se tiver o número correto de argumentos:
    else 
	{ 
        //verifica se cada caractere é uma letra do alfabeto:
		for (int i = 0, n = strlen(argv[1]); i < n; i++) 
		{ 
			if (!isalpha(argv[1][i])) 
			{ 
                //se não printa como usar o programa:
				printf("Usage: ./vigenere keyword (alphabetic characters)");
				return 1;
			} 			
		}
	} 
    
    // uma vez que o argv for correto, botar a "key" dentro da variável "key":
    string key = argv[1];
    //pega o tamanho da variável key:
    int keylen = strlen(key);
    // pede para o usuário um código para encriptar e armazena a respota em "plaintext":
    string plaintext = get_string("plaintext: ");
    //loop através do texto:
    printf("ciphertext: ");
    for (int i = 0, j = 0, n = strlen(plaintext); i < n; i++)
    {
        //pega a key para a letra:
        int letterKey = tolower(key[j % keylen]) - 'a';
        //verifica se a letra esta maíscula ou minúscula, encripta ela e a escreve:
        if islower(plaintext[i])
        {
            printf("%c", 'a' + (plaintext[i] - 'a' + letterKey) % 26);
            j++;
        }
        else if isupper(plaintext[i])
        {
            printf("%c", 'A' + (plaintext[i] - 'A' + letterKey) % 26);
            j++;
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
