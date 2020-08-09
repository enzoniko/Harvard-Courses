//bibliotecas:
#include <cs50.h>
#include <stdio.h>
//função main:
int main(void){  
    //variáveis:
    int height, j, i;
    //pega a altura da pirâmide:
    printf("How tall is the Pyramid? ");
    scanf("%d",&height);
    //verifica se a altura esta entre 1 e 8 inclusive:
    while(height < 1){
        printf("How tall is the Pyramid? ");
        scanf("%d",&height);
    }
    while(height > 8){
        printf("How tall is the Pyramid? ");
        scanf("%d",&height);
    }
    while(height == 0){
        printf("How tall is the Pyramid? ");
        scanf("%d",&height);
    }
    //pega a altura e divide em andares:
    for ( i = 0; i < height; i++){
        //escreve os espaços necessários em cada andar:
        for (j = 0; j < height - i - 1; j++)
            printf(" ");
        //escreve os hashtags necessários em cada andar:
        for ( j = 0; j < i + 1; j++)
            printf("#");
        //divide os andares:
        printf("\n");
        
    } 
}
