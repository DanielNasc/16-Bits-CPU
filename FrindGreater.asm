.data 
	vet: .word 13 20 422 100
	x: .word 5
.text 
	addi $t0 $zero 0
	addi $t1 $zero 0
	addi $t2 $zero 0
while:
    addi $s1 $zero 4
	beq $t0 $s1 saida
	lw $t3 $t0 vet
	slt $s0 $t2 $t3
	beq $s0 $zero maior
	add $t2 $t3 $zero
maior:
	addi $t1 $t1 1
	addi $t0 $t0 1
	j while
saida:
	sw $t2 x
    j saida