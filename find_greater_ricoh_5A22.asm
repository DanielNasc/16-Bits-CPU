.org $C000          ; Endereço de início do programa

vetor:
    .word 2, 8, 1, 6, 5, 3, 9, 4    ; Vetor de exemplo
tamanho:
    .word 8                        ; Tamanho do vetor

MAX_VALUE = $0000                  ; Variável para armazenar o maior valor encontrado
INDEX     = $0002                  ; Variável para rastrear o índice atual
TEMP      = $0004                  ; Variável temporária para comparação

    CLC                           ; Limpa o Carry Flag
    LDA #$00                      ; Carrega 0 em A
    STA MAX_VALUE                 ; Inicializa o valor máximo como 0

    LDX tamanho                    ; Carrega o tamanho do vetor em X
    DEX                            ; Decrementa X para obter o índice máximo

loop:
    CPX #$00                      ; Compara se X é igual a 0
    BEQ end                        ; Se X for 0, termina o loop

    LDA vetor, X                  ; Carrega o valor do vetor na posição X em A
    STA TEMP                      ; Armazena temporariamente o valor do vetor

    LDA MAX_VALUE                 ; Carrega o valor máximo atual em A
    CMP TEMP                      ; Compara o valor do vetor com o valor máximo atual

    BCC not_greater               ; Se o Carry Flag estiver limpo, o valor do vetor não é maior
    STA MAX_VALUE                 ; Atualiza o valor máximo com o valor do vetor

not_greater:
    DEX                            ; Decrementa X para avançar para o próximo elemento
    JMP loop                       ; Salta de volta para o início do loop

end:
    ; O valor máximo estará em MAX_VALUE
    ; Você pode usar essa informação para exibir ou realizar outras operações

    BRK                            ; Termina o programa

    .end                           ; Fim do programa
