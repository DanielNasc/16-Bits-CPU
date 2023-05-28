.data
    ARRAY: .word 2 8 6 23 3 9 4
    ARRAY_SIZE: .word 7
.vars
    REMAINING_AMOUNT          = 0000
    GREATER_ADDRESS           = 0002 # Adress of the greater element in the ARRAY
    CURRENT_VALUE_ADDR_ADRESS = 0004
.text
    # load address into accumulator
    laa ARRAY

   # load value from a address into a register
    ldr $x $a # x = array[0]
    # store register x into memory
    stx GREATER_ADDRESS 

    # add immediate
    addi $a 2 # next element address;  A = CURRENT_VALUE_ADDR_ADRESS + WORD_LEN
    # store accumulator into memory
    sta CURRENT_VALUE_ADDR_ADRESS

    # load value into accumulator
    lda REMAINING_AMOUNT
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
        # compare a register with accumulator and set specific flags
        cmp $x
        # branch if carry clear 
        bcc next

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
        end
