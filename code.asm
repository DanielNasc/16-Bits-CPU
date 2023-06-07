.data
    ARRAY: .word 2 8 6 23 3 9 4
    ARRAY_SIZE: .word 7
    REMAINING_AMOUNT:          .word 7 
    GREATER_ADDRESS:           .word 0
    CURRENT_VALUE_ADDR_ADRESS: .word 0
.text
    # load address into accumulator
    

   # load value from a address into a register
    ldr $x $a # x = array[0]
    # store register x into memory
    stx GREATER_ADDRESS 

    # add immediate
    addi $a 2 # next element address;  A = CURRENT_VALUE_ADDR_ADRESS + WORD_LEN
    # store accumulator into memory
    sta CURRENT_VALUE_ADDR_ADRESS

    # load value into accumulator
    laa ARRAY_SIZE
    ldr $a $a
    # subtract immediate
    subi $a 1
    # store accumulator into memory
    sta REMAINING_AMOUNT

    loop:
        # load value into x
        ldx REMAINING_AMOUNT
        # branch if equal zero
        beqz $x end

        # if Accumulator (GREATER) >= X (CURRENT), skip
        # load value into accumulator
        lda GREATER_ADDRESS
        # load value into y register
        ldy CURRENT_VALUE_ADDR_ADRESS # y = *CURRENT_VALUE_ADDR_ADRESS
        # load value from a address into a register
        ldr $x $y # x = VECTOR[I]
        # # branch if x is less than the accumulator
        blt $x next

        # store x value into memory
        stx GREATER_ADDRESS
    next:
        # add immediate
        addi $y 2 # A = CURRENT VALUE ADRESS + WORD_LEN
        # store accumulator into memory
        sta CURRENT_VALUE_ADDR_ADRESS

        # load a value into accumulator
        lda REMAINING_AMOUNT
        # subtract immediate
        subi $a 1
        # store accumulator into memory
        sta REMAINING_AMOUNT

        # jump
        j loop
    end:
        addi $a 1
        j end
