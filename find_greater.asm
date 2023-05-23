.data
    vetor: .word 2, 8, 6, 5, 3, 9, 4   # vetor de exemplo
    tamanho: .word 8                     # tamanho do vetor

.text
.globl main
main:
    la $t0, vetor       # carrega o endereço base do vetor em $t0
    lw $t1, tamanho     # carrega o tamanho do vetor em $t1
    addi $t1, $t1, -1   # subtrai 1 do tamanho para obter o índice máximo

    lw $t2, ($t0)      # carrega o primeiro elemento do vetor em $t2 (maior valor inicial)
    addi $t0, $t0, 4    # avança para o próximo elemento do vetor
loop:
    beqz, $t0,  end       # se o tamanho for zero, termina o loop
    lw $t3, 0($t0)      # carrega o próximo elemento do vetor em $t3

    slt $t4, $t3, $t2   # compara se $t3 é menor que $t2
    bnez $t4, not_greater # se $t3 não for maior que $t2, pula para not_greater
    move $t2, $t3       # se $t3 for maior que $t2, atualiza o valor máximo

not_greater:
    addi $t0, $t0, 4    # avança para o próximo elemento do vetor
    addi $t1, $t1, -1   # decrementa o tamanho
    j loop              # retorna para o início do loop

end:
    # O valor máximo estará em $t2
    li $v0, 1           # código de syscall para imprimir inteiro
    move $a0, $t2       # move o valor máximo para o registrador de argumento $a0
    syscall             # chama a syscall

    li $v0, 10          # código de syscall para sair do programa
    syscall             # chama a syscall
