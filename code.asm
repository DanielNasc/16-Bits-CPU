main:
    la $t0, vetor      
    lw $t1, tamanho    
    addi $t1, $t1, -1  

    lw $t2, 4($t0)     
    addi $t0, $t0, 4   

loop:
    beqz $t1, end      
    lw $t3, 0($t0)     

    slt $t4, $t3, $t2  
    beqz $t4, not_greater
    move $t2, $t3      

not_greater:
    addi $t0, $t0, 4   
    addi $t1, $t1, -1  
    j loop             
end:

    li $v0, 1          
    move $a0, $t2      
    syscall            
    li $v0, 10         
    syscall            
