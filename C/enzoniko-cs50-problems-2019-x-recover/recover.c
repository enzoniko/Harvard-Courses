// Bibliotecas:
#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>

// Função main que pede um argumento:
int main(int argc, char *argv[])
{
    // Inicializa e guarda o nome do arquivo:
    char *image = argv[1];

    // Aceita apenas um argumento de linha
    if (argc != 2)
    {
        // Se tiver mais que um printa como usar o programa:
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }

    // Abre o arquivo de entrada
    FILE *inptr = fopen(image, "r");

    // Se a imagem não pode ser aberta para leitura, falha:
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", image);
        return 2;
    }

    // Inicializa o buffer da busca pela identificação do JPG parte por parte
    // Usando 'unsigned' de 0 à 255:
    unsigned char buffer[512];

    // Inicializa as variáveis de rastreamento:
    int openFileTracker = 0;
    int jpegTracker = 0;

    // Inicializa a variável "filename" e a variável "img_file":
    char filename[10];
    FILE *img_file;


    // Loop através da leitura do arquivo de imagem através de blocos de 512 bytes até chegar no fim do arquivo
    // ...Usando o valor de retorno de "fread" para avisar se o bloco completo foi lido ou falhou ou seja, chegou no fim do arquivo
    // ...Usando a expressão booleana do "while loop" retornando falso para finalizar o loop qunado chegar no final do arquivo:
    while (fread(&buffer, 512, 1, inptr))
    {
        // Verifica os 4 bytes iniciais de um dos pedaços de "buffer" para ver se corresponde ao começo de um JPEG:
        if (buffer[0] == 0xff &&
            buffer[1] == 0xd8 &&
            buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            // Ja temos um JPEG aberto?
            // Se tivermos:
            if (openFileTracker)
            {
                // Fecha o arquivo que foi aberto antes:
                fclose(img_file);

                // Deixa "openFileTracker" como falso (por segurança):
                openFileTracker = 0;

                // Cria um novo nome de arquivo:
                sprintf(filename, "%03d.jpg", jpegTracker);

                // Aplica e abre esse arquivo novo:
                img_file = fopen(filename, "a");

                // Deixa "openFileTracker" como verdadeiro:
                openFileTracker = 1;

                // Incrementa o nosso rastreador de nome arquivo:
                jpegTracker++;
            }

            // Se não tivermos um JPEG aberto:
            if (!openFileTracker)
            {
                // Abre e da nome a um novo arquivo:
                sprintf(filename, "%03d.jpg", jpegTracker);
                img_file = fopen(filename, "w");

                // Agora temos um arquivo aberto:
                openFileTracker = 1;

                jpegTracker++;
            }

            // Escreve o "buffer" no arquivo:
            fwrite(&buffer, 512, 1, img_file);
        }

        // Se não for o começo de um novo JPEG:
        else
        {
            if (openFileTracker)
            {
                // Escreve o "buffer" no arquivo:
                fwrite(&buffer, 512, 1, img_file);
            }
        }
    }

    // Se o "while loop" acabou então chegamos no fim do arquivo
    // Fecha o arquivo inicial de imagem:
    fclose(inptr);

    // Fecha qualquer arquivo JPEG aberto:
    fclose(img_file);

    return 0;
}