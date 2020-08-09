// Bibliotecas:
#include <stdio.h>
#include <stdlib.h>
#include "bmp.h"
// Função main que pede três argumentos:
int main(int argc, char *argv[])
{

    // Inicializa e guarda os nomes dos arquivos:
    char *infile = argv[2];
    char *outfile = argv[3];

    // Verifica se o argumento de input tem tamanho apropriado:
    if (argc != 4)
    {
        // Se o tamanho não for apropriado printa como usar o programa:
        printf("Usage: ./resize n infile outfile\n");
        return 1;
    }

    // Verifica se o fator para redimensionar(n) tem um valor apropriado:
    int n = atoi(argv[1]);
    if (n < 0 || n > 100)
    {
        // Se não for um número entre 0 e 100 printa que "n" tem que estar entre esses valores:
        printf("n must be possitive and less than or equal to 100\n");
        return 1;
    }

    // Abre o arquivo de entrada:
    FILE *inptr = fopen(infile, "r");

    // Verifica se o arquivo de entrada existe ou é possível de ler.
    // Se não for falha:
    if (inptr == NULL)
    {
        printf("Could not open %s.\n", infile);
        return 2;
    }

    // Abre o arquivo de saída:
    FILE *outptr = fopen(outfile, "w");

    // Verifica se o arquivo de saída existe ou é possível de ler.
    // Se não for falha:
    if (outptr == NULL)
    {
        fclose(inptr);
        printf("Could not create %s.\n", outfile);
        return 3;
    }

    // Declara os "header files" dos arquivos de entrada e de saída:
    BITMAPFILEHEADER in_bf;
    BITMAPINFOHEADER in_bi;
    BITMAPFILEHEADER out_bf;
    BITMAPINFOHEADER out_bi;

    // Lê os arquivos BITMAPFILEHEADER & BITMAPINFOHEADER do arquivo de entrada:
    fread(&in_bf, sizeof(BITMAPFILEHEADER), 1, inptr);
    fread(&in_bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // Verifica que o arquivo de entrada é um BMP 4.0 descomprimido de 24-bit preferencialmente:
    if (in_bf.bfType != 0x4d42 || in_bf.bfOffBits != 54 || in_bi.biSize != 40 ||
        in_bi.biBitCount != 24 || in_bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        printf("Unsupported file format.\n");
        return 4;
    }

    // Gera os valores iniciais dos arquivos de cabeçalho do arquivo de saída (pré-redimensionamento):
    out_bf = in_bf;
    out_bi = in_bi;

    // Muda os valores de altura e largura do cabeçalho de informações do arquivo de sáida baseado em "n":
    out_bi.biWidth = in_bi.biWidth * n;
    out_bi.biHeight = in_bi.biHeight * n;

    // Calcula os valores de padding do arquivo de entrada e saída para poder calcular o tamanho da imagem do arquivo de saída:
    int in_padding = (4 - (in_bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int out_padding = (4 - (out_bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // Modifica biSizeImage no cabeçalho de informações do arquivo de saída:
    out_bi.biSizeImage = (out_bi.biWidth * sizeof(RGBTRIPLE) + out_padding) * abs(out_bi.biHeight);

    // Modifica bfSize no arquivo de cabeçalho do arquivo de saída:
    out_bf.bfSize = out_bi.biSizeImage + 54;


    // Escreve os valores de BITMAPFILEHEADER & BITMAPTINFOHEADER para o arquivo de saída:
    fwrite(&out_bf, sizeof(BITMAPFILEHEADER), 1, outptr);
    fwrite(&out_bi, sizeof(BITMAPINFOHEADER), 1, outptr);

    // screve os dados redimensionados para o arquivo de saída:
    // Loop entre as linhas do arquivo de entrada:
    for (int i = 0, biHeight = abs(in_bi.biHeight); i < biHeight; i++)
    {
        // Redimensionamento vertical: Escreve cada linha "n" vezes:
        for (int v = 0; v < n; v++)
        {
            // Repete em cada pixel das linhas do arquivo de Entrada:
            for (int j = 0; j < in_bi.biWidth; j++)
            {
                // Armazenamento temporário:
                RGBTRIPLE triple;

                // Lê RGB triple do Arquivo de entrada:
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

                // Redimensionamento horizontal: Escreve RGB triple no arquivo de saída:
                for (int h = 0; h < n; h++)
                {
                    fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                }
            }

            // Se o arquivo de entrada tive padding, pular o padding:
            fseek(inptr, in_padding, SEEK_CUR);

            // Adiciona qualquer padding necessário no arquivo de saída:
            for (int p = 0; p < out_padding; p++)
            {
                fputc(0x00, outptr);
            }

            // Move o ponteiro para o começo da linha (para rescrever a linha):
            // É usado sizeof(RGBTRIPLE) pois a largura está em pixels e não em bytes.
            // fseek move o ponteiro para uma localização onde tem um byte, e esta lendo triples que são pixels.
            // 1 pixel = sizeof(RGBTRIPLE) que é três tipos...enquanto... 1 padding = 1 byte.
            fseek(inptr, -((in_bi.biWidth * sizeof(RGBTRIPLE)) + in_padding), SEEK_CUR);
        }

        // Move o ponteiro pra frente até o final da ultima linha, para lermos a proxima linha:
        fseek(inptr, (in_bi.biWidth * sizeof(RGBTRIPLE)) + in_padding, SEEK_CUR);
    }

    // Fecha o arquivo de entrada:
    fclose(inptr);

    // Fecha o arquivo de saída:
    fclose(outptr);

    return 0;
}