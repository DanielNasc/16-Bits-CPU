.data
    vetor: .word 2, 8, 6, 23, 3, 9, 4   # vetor de exemplo
    tamanho: .word 8                     # tamanho do vetor

.text
main:
    lj 	vetor       	# carrega o endereço base do vetor em $R1
    ia  $jn0
    lda tamanho     	# carrega o tamanho do vetor em R2
    ia  $jn1
    jc  $jn1, -1   	    # subtrai 1 do tamanho para obter o índice máximo

    ld 	0($jn0)      	# carrega o primeiro elemento do vetor em $R3 (maior valor inicial)
    ia $jn2
    jc $jn0, 4    	    # avança para o próximo elemento do vetor
loop:
    i   $iu,  $jn1
    cmpi    0
    geb	end       	    # se o tamanho for zero, termina o loop
    ld 	0($jn0)      	# carrega o próximo elemento do vetor em $R4
    ia $jn3

    i   $iu,  $jn2
    cmp $jn3                # seta carry flag se A >= R4
    geby    not_greater	    # se $R4 não for maior que $R3, pula para not_greater
    i   $jn2, $jn3       	# se $R4 for maior que $R3, atualiza o valor máximo

not_greater:
    jc 	$jn0, 4    	    # avança para o próximo elemento do vetor
    jc 	$jn1, -1   	    # decrementa o tamanho
    d 	loop            # retorna para o início do loop

end:
   
   
