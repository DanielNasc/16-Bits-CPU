.data
    vetor: .word 2 8 6 23 3 9 4  
    tamanho: .word 8                    

.text
main:
    lja 	vetor       
    ia  $jn0
    lda tamanho     
    ia  $jn1
    jci  $jn1 -1   	   

    ld 	0($jn0)      
    ia $jn2
    jci $jn0 4    	   
loop:
    i   $iu  $jn1
    cmpi    0
    yibi	end       	   
    ld 	0($jn0)      
    ia $jn3

    i   $iu  $jn2
    cmp $jn3               
    geb    not_greater	   
    i   $jn2 $jn3       

not_greater:
    jci 	$jn0 4    	   
    jci 	$jn1 -1   	   
    d 	loop           

end:
   