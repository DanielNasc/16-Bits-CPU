.data
    vetor: .word 2, 8, 6, 23, 3, 9, 4   # vetor de exemplo
    tamanho: .word 8                     # tamanho do vetor

.text
.globl main
main:
    la 	 vetor       	# carrega o endereço base do vetor em $R1
    mova R1
    lwa 	 tamanho     	# carrega o tamanho do vetor em R2
    mova R2
    addi R2, 	-1   	# subtrai 1 do tamanho para obter o índice máximo

    lw 	0($R1)      	# carrega o primeiro elemento do vetor em $R3 (maior valor inicial)
    mova R3
    addi $R1, 	4    	# avança para o próximo elemento do vetor
loop:
    move A R2
    cmpi  0
    beq	end       	# se o tamanho for zero, termina o loop
    lw 	0($R1)      	# carrega o próximo elemento do vetor em $R4
    mova R4

    move A R3
    cmp  R4   # seta carry flag se A >= R4
    bcc not_greater	# se $R4 não for maior que $R3, pula para not_greater
    move R3, 	R4       	# se $R4 for maior que $R3, atualiza o valor máximo

not_greater:
    addi 	R1, 	4    	# avança para o próximo elemento do vetor
    addi 	R2, 	-1   	# decrementa o tamanho
    j 	 loop              	# retorna para o início do loop

end:
   rts