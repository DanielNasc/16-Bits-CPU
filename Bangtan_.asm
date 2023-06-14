.data 
	vet: .word 13 20 422 100
	x: .word 5
.text 
	jci $jn0 $yeong 0
	jci $jn1 $yeong 0
	jci $jn2 $yeong 0
while:
    jci $sg1 $yeong 4
	jge $jn0 $sg1 saida
	ld $jn3 $jn0 vet
	jg $sg0 $jn2 $jn3
	jge $sg0 $yeong maior
	jc $jn2 $jn3 $yeong
maior:
	jci $jn1 $jn1 1
	jci $jn0 $jn0 1
	d while
saida:
	jd $jn2 x
    d saida