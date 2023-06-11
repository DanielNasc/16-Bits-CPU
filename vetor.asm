.data 
	vet: .word 13 20 422 100
	x: .word 5
.text 
	addi $t0 $zero 0
	addi $t1 $zero 0
	addi $t2 $zero 0
while:
	beq $t0 4 saida
	lw $t3 vet($t1)
	slt $s0 $t3 $t2
	beq $s0 $zero maior
	addi $t1 $t1 4
	addi $t0 $t0 1
	j while
maior:
	add $t2 $t3 $zero
	addi $t1 $t1 4
	addi $t0 $t0 1
	j while
saida:
	sw $t2 x($zero)

	
	
