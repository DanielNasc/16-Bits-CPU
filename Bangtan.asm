.data
    ARRAY: .word 2 8 6 23 3 9 4
    ARRAY_SIZE: .word 7
    REMAINING_AMOUNT:          .word 7 
    GREATER_ADDRESS:           .word 0
    CURRENT_VALUE_ADDR_ADRESS: .word 0
.text
    toni  $jn0 $zero 	ARRAY       	
    ld 	 $jn1 	ARRAY_SIZE     	
    dli $jn1 	$jn1 	1   	

    dli 	 $jn2 	$jn0
    jci $jn0 	$jn0 	4    	
loop:
    yibi $jn1  	end       	
    dli 	 $jn3 	$jn0

    slt  $jn4 	$jn3 	$jn2   	
    yabi $jn4 	not_greater	
    ton $jn2 	$jn3    $zero

not_greater:
    jci $jn0 	$jn0 	4    	
    dli $jn1 	$jn1 	1   	
    d 	 loop              	

end:
    
    jci $jn0 $jn0 1
    d end         		
