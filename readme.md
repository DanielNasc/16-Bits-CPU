# Processador Bangtan

#### Formato das Instruções
| Tipo de Instrução | OpCode | Registradores | Imediato |
| :---------------: | :----: | :-----------: | :------: |
| Chu-Format | 4 bits | 12 bits | - |
| Deol-Format | 4 bits | 8 bits | 4 bits |
| Hobi-Format | 4 bits | 4 bits | 8 bits |
| Jeon-Format | 4 bits | - | 12 bits |

### Registradores
8 registradores
Os registradores são procedidos de $ nas instruções
Duas formas de representação:
Numero do registrador. $0 até $7
Usando os nomes equivalentes (ver abaixo). Ex: $jn1, $iu
| # do Reg. | Nome | Descrição |
| :-------: | :--: | :-------: |
| 0 | $zero | Sempre 0 |
| 1 | $jn0 | Acumulador |
| 2 | $jn0 | Registrador de uso geral |
| 3 | $jn1 | Registrador de uso geral |
| 4 | $sp | Stack Pointer |
| 5 | $ps | Program Status |
| 6 | $bj | Return Address |
| 7 | $bb | Return Buffer |

### Declaração de Dados
Seção do programa identificado pela diretiva .data
Os nomes declarados das variáveis são usados no programa. Dados guardados na
memória principal (RAM)

### Código
Seção do programa identificado pela diretiva .text
Contêm o código do programa (instruções).
Ponto de inicio do código marcado pelo label main:
O final da main deve usar a chamada de saída do sistema.

### Instruções MIPS/6502 >>> Bangtan

| Nome da Instrução (MIPS) | Nome da Instrução (Bangtan) | Inspiração
| :----------------------: | :-------------------------: | :--------: |
| **la** (load address) | **lj** | lodeu juso
| - | **lja** | -
| **lw** (load word) | **ld** | lodeu dan-eo"
| **lda** (load accumulator) | **lal** | lodeu A lejiseuteo
| **ldx** (load register x) | **lj0** | lodeu JN0 lejiseuteo
| **ldy** (load register jn1) | **lj1** | lodeu JN1 lejiseuteo
| **ldr** (load from address in register) | **llj** | lejiseuteo lodeu juso
| - (load from accumulator) | **la** | load into accumulator
| **sw** (store word)| **jd** | jeojang dan-eo
| **sta** (store accumulator) | **sal** | seuto-eo A lejiseuteo
| **stx** (store register x) | **sj0** | seuto-eo JN0 lejiseuteo
| **sty** (store register y) | **sj1** | seuto-eo JN1 lejiseuteo
| - (store into accumulator) | **ja** | store into accumulator
| - (store immediate into accumulator) | **jai** | store immediate into accumulator
| **add** | **jc** | -
| **addi** | **jci** | jeugsi chuga
| **sub** | **dl** | deolda
| **subi** | **dli** | -
| **b** (branch) | **g** | -
| **bcc** (branch if carry clear) | **geb** | kaeli keullin bungi
| **beqz** (branch if equal zero) | **yibi** | yeong imyeon bungi
| **bnez** (branch if not equal zero) | **yabi** | yeongi anin gyeong-u bungi
| **blt** (branch if less than accumulator) | **blt** | -
| **move** | **i** | idonghada
| **j** (jump) | **d** | doyag
| **jr** | **dr** | -
| **jal** | **dal** | -
| **and** | **geu** | geuligo
| **or** | **ton** | ttoneun
| **nor** | **aton** | -
| - | **cmp** | comparator
| - | **cmpi** | comparator with immediate 
| **clc** (clear carry) | **kk** | keullieo kaeli


### Leitura/Escrita
Acesso a memória RAM apenas com instruções de leitura e escrita.
Todas outras instruções usam registradores como operando.

#### Leitura/Escrita de endereçamento direto
##### Leitura:
- `ld registrador1, registrador2`

copia word(2 bytes) da posição da RAM dada pelo registrador2, para o registrador1.
- `ldi registrador, valor`

carrega o valor para o registrador de destino.
- `la registrador`

copia word (2 bytes) do acumulador($iu), para o registrador dado.

##### Escrita:
- `jd registrador, posição_da_RAM`

escreve a word do registrador dado na posição da RAM dada.
- `ja registrador`

copia word (2 bytes) do registrador dado, para o acumulador($iu).
- `jai valor`

carrega o valor para o acumulador($iu).

##### Exemplo:
```assembly
.data
    var1:   .word   23
    
.text
main:
    ld  $jn0,   var1    # carrega o conteúdo de var1 em $jn0.
    ldi $jn1,   8       # $jn1 = 8
    la  $jn0            # carrega o conteúdo do acumulador($iu) em $jn0.
    jd  $jn1,   var1    # carrega o conteúdo de $jn1 em var1.
    ja  $jn0            # carrega o conteúdo de $jn0 em $iu(acumulador).
    jai 7               # $iu(acumulador) = 7
```
#### Leitura/Escrita de endereçamento indireto e por base 
##### Leitura
- `lj registrador, label`

copia o endereço do label na    memória para o registrador dado.
- `lja label`

copia o endereço do label na memória para o acumulador($iu).
- **Endereçamento indireto**

`ld registrador1, (registrador2)`
carrega a word que está no endereço dado pelo registrador2, para o registrador1.
- **Endereçamento por base**

`ld registrador1, offset(registrador2)`
carrega a word que está no endereço (registrador2 + offset) para o registrador1.
**obs: o offset pode ser negativo**
- **Endereçamento indireto (acumulador)**

`la (registrador)`
carrega a word que está no acumulador($iu), para o endereço dado pelo registrador.
- **Endereçamento por base (acumulador)**

`la offset(registrador)`
carrega a word que está no acumulador($iu), para o endereço (registrador + offset).
**obs: o offset pode ser negativo**

##### Escrita
- **Endereçamento indireto**

`jd registrador1, (registrador2)`
copia a word no registrador1 para posição de memória de endereço dado pelo registrador2.
- **Endereçamento por base (acumulador)**

`jd registrador1, offset(registrador2)`
copia a word no registrador1 para posição de memória de endereço dado por (registrador2 + offset).
**obs: o offset pode ser negativo**
- **Endereçamento indireto**

`ja (registrador)`
copia a word que está na posição de memória dada pelo registrador, para o do acumulador($iu).
- **Endereçamento por base (acumulador)**
`ja offset(registrador)`

copia a word que está na posição de memória (registrador + offset), para o do acumulador($iu).
**obs: o offset pode ser negativo**

#### Movimentação
- `i registrador0, registrador1`

copia o valor do registrador1 para o registrador0.

##### Exemplo:
```assembly
    i   $jn0,   $jn1    #$jn0 = $jn1
```
#### Aritméticas
Todos operandos são registradores
- `jc registrador1, registrador2`

salva o resultado da soma do registrador1 com o registrador2 no acumulador($iu).
##### Exemplo:
```assembly
    jc   $jn0,   $jn1    #$iu = $jn0 + $jn1
```
- `jci registrador, imediato`

salva o resultado da soma do registrador com o imediato no acumulador($iu).
##### Exemplo:
```assembly
    jci   $jn0,    4    #$iu = $jn0 + 4
    jci   $jn1,    -7    #$iu = $jn1 + (-7)
```
- `dl registrador1, registrador2`

salva o resultado da subtração do registrador1 com o registrador2 no acumulador($iu).
##### Exemplo:
```assembly
    dl   $jn0,   $jn1    #$iu = $jn0 - $jn1
```
- `dli registrador, imediato`

salva o resultado da subtração do registrador com o imediato no acumulador($iu).
##### Exemplo:
```assembly
    dli   $jn0,    4    #$iu = $jn0 - 4
    dli   $jn1,    -7    #$iu = $jn1 - (-7)
```
#### Lógicas
- `geu registrador1, registrador2`

guarda o resultado da operação lógica correspondente ao AND entre o registrador1 e o registrador2 no acumulador($iu).
- `ton registrador1, registrador2`

guarda o resultado da operação lógica correspondente ao OR entre o registrador1 e o registrador2 no acumulador($iu).
- `aton registrador1, registrador2`

guarda o resultado da operação lógica correspondente ao NOR entre o registrador1 e o registrador2 no acumulador($iu).

#### Desvios
#### Desvio Incondicional
- `g label`

muda o registrador PC(registrador que guarda o endereço da próxima instrução
a ser executada) para o valor do label.
- `d label`

muda o registrador PC(registrador que guarda o endereço da próxima instrução
a ser executada) para o valor do label.
- `dr registrador`

muda o registrador PC(registrador que guarda o endereço da próxima instrução
a ser executada) para o endereço contido no registrador.

#### Desvio Condicional
- `yibi label`

Desvia para a label, se: a flag zero estiver setada.
- `yabi label`

Desvia para a label, se: a flag zero não estiver setada.
- `geb label`

Desvia para a label, se: a carry flag estiver setada.

#### Chamada de subrotina
- `dal label`

desvia para o label da subrotina e copia o PC para o registrador RA.
- `dr ra`

desvia para o endereço contido em RA usado para fazer o retorno da subrotina para o programa.
**Obs: se uma subrotina for chamar outra subrotina, ou é recursiva, o endereço em RA
será sobrescrito, ele deveria então ser empilhado para que ele possa ser preservado e recuperado ao termino das chamadas para dar continuidade ao programa normalmente.**

#### Alterador de Flags
- `cmp registrador`

Compara o valor no registrador dado com o valor no acumulador($iu) utilizando a aperação aritmética de soma, alterando as flags com base no resultado.
- `cmpi valor`

Compara o valor dado com o valor do acumulador($iu) utilizando operações aritméticas de soma e subtração, alterando as flags com base no resultado.

#### Flags
`Zero` : setada se registrador e o acumulador forem iguais.
`Carry` : setada se o registrador for maior ou igual ao acumulador.

### Controle da ALU
| Instruction Opcode | Opcode | ALUOp | Instruction Operation | Desired ALU Action | ALU Control Input |
| :---------------: | :-----: | :--: | :-------------: | :-------: | :-----: |
| Deol-Format | - | 01 | lj | add | 0010 |
| Jeon-Format | - | 10 | lja | add | 0010 |




