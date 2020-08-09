#include <stdbool.h>
#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#include "dictionary.h"


// Tamanho da Hashtable:
#define SIZE 1000000

// Cria os nodes para as listas linkadas:
typedef struct node
{
    char word[LENGTH+1];
    struct node* next;
}
node;

// Cria a hashtable:
node* hashtable[SIZE] = {NULL};

// Cria a função hash:
int hash (const char* word)
{
    int hash = 0;
    int n;
    for (int i = 0; word[i] != '\0'; i++)
    {
        // Caso alfabético:
        if(isalpha(word[i]))
            n = word [i] - 'a' + 1;

        // Caso de vírgula:
        else
            n = 27;

        hash = ((hash << 3) + n) % SIZE;
    }
    return hash;
}

// Cria variável global para a contagem do tamanho:
int dictionarySize = 0;

// Carrega o dicionário na memória. Retorna True se foi sucedido, se não retorna False:
bool load(const char* dictionary)
{
    // Abre o dicionário:
    FILE* file = fopen(dictionary, "r");
    if (file == NULL)
        return false;

    // Cria uma lista para armazenar as palavras:
    char word[LENGTH+1];

    // Scaneia através do arquivo, carregando cada palavra na hashtable:
    while (fscanf(file, "%s\n", word)!= EOF)
    {
        // Incrementa o tamanho do dicionário:
        dictionarySize++;

        // Distribui memória para a nova palavra:
        node* newWord = malloc(sizeof(node));

        // Bota a palavra no novo node:
        strcpy(newWord->word, word);

        // Encontra em qual índice da lista a palavra deve ir:
        int index = hash(word);

        // Se a hashtable estiver vazia nesse índice, bota a palavra:
        if (hashtable[index] == NULL)
        {
            hashtable[index] = newWord;
            newWord->next = NULL;
        }

        // Se não, acrescenta:
        else
        {
            newWord->next = hashtable[index];
            hashtable[index] = newWord;
        }
    }

    // Fecha o arquivo:
    fclose(file);

    // Retorna True se foi sucedido:
    return true;
}

// Retorna True se a palavra estiver no dicionário, se não retorna False:
bool check(const char* word)
{
    // Cria uma variável temporária que armazena uma versão minúscula da palavra:
    char temp[LENGTH + 1];
    int len = strlen(word);
    for(int i = 0; i < len; i++)
        temp[i] = tolower(word[i]);
    temp[len] = '\0';

    // Encontra em qual índice da lista a palavra deve ir:
    int index = hash(temp);

    // Se a hashtable estiver vazia nesse índice, retorna False:
    if (hashtable[index] == NULL)
    {
        return false;
    }

    // Cria cursor para comparar com a palavra:
    node* cursor = hashtable[index];

    // Se a hashtable não estiver vazia no índice, passa por cada palavra e compara:
    while (cursor != NULL)
    {
        if (strcmp(temp, cursor->word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }

    // Se não achar a palavra, retorna False:
    return false;
}

// Retorna o número de palavras no dicionário se ele estiver carregado, se não retorna zero:
unsigned int size(void)
{
    // Se o dicionário estiver carregado, retorna o número de palavras:
    if (dictionarySize > 0)
    {
        return dictionarySize;
    }

    // Se ele não estiver carregado, retorna zero:
    else
        return 0;
}

// Descarrega o dicionário da memória. Retorna True se for bem sucedido, se não retorna False:
bool unload(void)
{
    // Cria uma variável para ir através do índice:
    int index = 0;

    // Passa por toda a lista da hashtable:
    while (index < SIZE)
    {
        // Se a hashtable estiver vazia no índice, vai para o próximo índice:
        if (hashtable[index] == NULL)
        {
            index++;
        }

        // Se a hashtable não estiver vazia, passa por cada node e libera a memória:
        else
        {
            while(hashtable[index] != NULL)
            {
                node* cursor = hashtable[index];
                hashtable[index] = cursor->next;
                free(cursor);
            }

            // Uma vez que a hashtable estiver vazia no índice, vai para o próximo índice:
            index++;
        }
    }

    // Retorna True se bem sucedido:
    return true;
}
// Fim!