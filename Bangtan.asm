.data
    vetor: .word 2, 8, 6, 23, 3, 9, 4   # vetor de exemplo
    tamanho: .word 8                     # tamanho do vetor

.text
main:
    lj 	 $jn0, 	vetor       	# carrega o endereço base do vetor em $t0
    ld 	 $jn1, 	tamanho     	# carrega o tamanho do vetor em $t1
    jc 	 $jn1, 	-1   		# subtrai 1 do tamanho para obter o índice máximo

    ld 	 $jn2, 	($jn0)      	# carrega o primeiro elemento do vetor em $t2 (maior valor inicial)
    jc   $jn0, 	4    		# avança para o próximo elemento do vetor
loop:
    yibi $jn1,  end       	# se o tamanho for zero, termina o loop
    ld 	 $jn3, 	0($jn0)      	# carrega o próximo elemento do vetor em $t3

    migs $jn4	$jn3, 	$jn2   	# compara se $t3 é menor que $t2
    yabi $jn4, 	not_greater	# se $t3 não for maior que $t2, pula para not_greater
    i	 $jn2, 	$jn3       	# se $t3 for maior que $t2, atualiza o valor máximo

not_greater:
    jc 	$jn0, 	4    		# avança para o próximo elemento do vetor
    jc 	$jn1, 	-1   		# decrementa o tamanho
    d 	 loop              	# retorna para o início do loop

end:
   
