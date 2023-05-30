.data
    ARRAY: .word 2 8 6 23 3 9 4
    ARRAY_SIZE: .word 7
.vars
    REMAINING_AMOUNT          = 0000
    GREATER_ADDRESS           = 0002 
    CURRENT_VALUE_ADDR_ADRESS = 0004
.text
    lja ARRAY
   
    llj $jn0 $iu 
    sj0 GREATER_ADDRESS 

    jci $iu 2 
    sal CURRENT_VALUE_ADDR_ADRESS

    lal REMAINING_AMOUNT
    dli $iu 1
    sal REMAINING_AMOUNT

    loop:
        lj0 REMAINING_AMOUNT
        yabi $jn0 end

        lal GREATER_ADDRESS
        lj1 CURRENT_VALUE_ADDR_ADRESS 
        llj $jn0 $jn1 
        kk
        cmp $jn0
        geb next

        sj0 GREATER_ADDRESS
    next:
        jci $jn1 2 
        sal CURRENT_VALUE_ADDR_ADRESS

        lal REMAINING_AMOUNT
        dli $iu 1
        sal REMAINING_AMOUNT

        d loop
    end:
        jci $iu 1
        d end
