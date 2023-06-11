.data
    ARRAY: .word 2, 8, 6, 23, 3, 9, 4   # vetor de exemplo
    ARRAY_SIZE: .word 8                     # tamanho do vetor
    I:          .word 0
    GREATER:           .word 0
.text
.globl main
main:
    ori $s0 	 $zero 	ARRAY       # $s0 = &vetor[0]
    lw 	 $t0 $s0 0                  # $t0 = vetor[0]
    ori $s1 $zero GREATER           # $s1 = &maior
    sw   $t0 $s1 0                  # maior = vetor[0]
    addi $s0 $s0 1                  # $s0 = &vetor[1]

    # store 1 in I address
    ori $s2 $zero I                  # $s2 = &i
    ori $t3 $zero 1                 # $t3 = 1
    sw $t3 $s2 0                    # i = 1

    # get array size
    ori $s3 $zero ARRAY_SIZE        # $s3 = &array_size
    lw $s3 $s3 0                    # $s3 = array_size

    loop:
        lw $t0 $s2 0                # $t0 = i
        beq $t0 $s3 end             # if i == array_size goto end

        lw $t0 $s0 0                # $t0 = vetor[i]
        