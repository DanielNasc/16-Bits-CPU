.data
    vetor: word 2 8 6 23 3 9 4
    tamanho: word 8

.text
main:
    lj 	 $jn0 	vetor
    ld 	 $jn1 	tamanho
    jc 	 $jn1 	-1

    ld 	 $jn2 	($jn0)
    jc   $jn0 	4
loop:
    yibi $jn1  end
    ld 	 $jn3 	0($jn0)

    migs $jn4	$jn3 	$jn2
    yabi $jn4 	
    i	 $jn2 	$jn3

not_greater:
    jc 	$jn0 	4
    jc 	$jn1 	-1
    d 	 loop

end:
   
