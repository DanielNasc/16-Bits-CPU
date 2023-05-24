# Bangtan

#### Formato das Instruções
| Tipo de Instrução | OpCode | Registradores | Imediato |
| :---------------: | :----: | :-----------: | :------: |
| Chu-Format | 4 bits | 12 bits | - |
| Deol-Format | 4 bits | 4 bits | 8 bits |
| Jeon-Format | 4 bits | - | 12 bits |
| Hope-Format | 4 bits | 8 bits | 4 bits |

### Registradores
16 registradores
Os registradores são procedidos de $ nas instruções
Duas formas de representação:
Numero do registrador. $0 até $15
Usando os nomes equivalentes (ver abaixo). Ex: $jn1, $iu
| # do Reg. | Nome | Descrição |
| :-------: | :--: | :-------: |
| 0 | $rm | (values) das expressões de avaliação e resultados de funções.
|1 ~ 2 | $sg0 - $sg1 | (arguments) Primeiros dos parâmetros para subrotinas.
|3 ~ 8 | $jn0 - $jn5 | Variáveis temporárias.
|9 ~ 11 | $jk0 - $jk2 | Valores salvos que representam os resultados computados finais.
|12 | $v | (Return address) Retorna para o endereço.
|13 | $iu | (Accumulator) Registrador acumulador.

### Declaração de Dados
Seção do programa identificado pela diretiva .data
Os nomes declarados das variáveis são usados no programa. Dados guardados na
memória principal (RAM)

### Código
Seção do programa identificado pela diretiva .text
Contêm o código do programa (instruções).
Ponto de inicio do código marcado pelo label main:
O final da main deve usar a chamada de saída do sistema.

### Instruções MIPS >>> Bangtan
#
| Nome da Instrução (MIPS) | Nome da Instrução (Bangtan) | Inspiração
| :----------------------: | :-------------------------: | :--------: |
| **la** (load address) | **lj** | lodeu juso
| **lw** (load word) | **ld** | lodeu dan-eo
| **li** (load immediate) | **ldi** | -
| - (load into accumulator) | **la** | load into accumulator
| **sw** (store word)| **jd** | jeojang dan-eo
| - (store into accumulator) | **ja** | store into accumulator
| - (store immediate into accumulator) | **jai** | store immediate into accumulator
| **add** | **jc** | -
| **addi** | **jci** | jeugsi chuga
| **sub** | **dl** | deolda
| **subi** | **dl** | deolda
| **beq** | **geb** | gat-eumyeon bungi
| **bcc** | **ggb** | kaeli keullin bungi
| **beqz** | **yibi** | yeong imyeon bungi
| **bnez** | **yabi** | yeongi anin gyeong-u bungi
| **slt** | **migs** | miman-in gyeong-u seoljeong
| **move** | **i** | idonghada
| **j** | **d** | doyag

### Leitura/Escrita
Acesso a memória RAM apenas com instruções de leitura e escrita.
Todas outras instruções usam registradores como operando.

#### Leitura/Escrita de endereçamento direto
##### Leitura:
- `ld registrador, posição_da_RAM`
 copia word(2 bytes) da posição da RAM dada, para o registrador.
- `ldi registrador, valor`
carrega o valor para o registrador de destino.
- `la registrador`
copia word (2 bytes) do acumulador, para o registrador dado.

##### Escrita:
- `jd registrador, posição_da_RAM`
escreve a word do registrador dado na posição da RAM dada.
- `ja registrador`
copia word (2 bytes) do registrador dado, para o acumulador.
- `jai valor`
carrega o valor para o acumulador.

##### Exemplo:
#
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
- `lj label`
escreve a word do registrador dado na posição da RAM.
- **Endereçamento indireto**
`ld registrador1, (registrador2)`
carrega a word que está no endereço dado pelo registrador2, para o registrador1.
- **Endereçamento por base**
`ld registrador1, offset(registrador2)`
carrega a word que está no endereço (registrador2 + offset) para o registrador1.
**obs: o offset pode ser negativo**
- **Endereçamento indireto (acumulador)**
`la (registrador)`
carrega a word que está no acumulador, para o endereço dado pelo registrador.
- **Endereçamento por base (acumulador)**
`la offset(registrador)`
carrega a word que está no acumulador, para o endereço (registrador + offset).
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
copia a word que está na posição de memória dada pelo registrador, para o do acumulador.
- **Endereçamento por base (acumulador)**
`ja offset(registrador)`
copia a word que está na posição de memória (registrador + offset), para o do acumulador.
**obs: o offset pode ser negativo**

#### Movimentação
- `i registrador0, registrador1`
- copia o valor do registrador1 para o registrador0.

##### Exemplo:
#
```assembly
    i   $jn0,   $jn1    #$jn0 = $jn1
```

### Controle da ALU
| Instruction Opcode | ALUOp | Instruction Operation | Desired ALU Action | ALU Control Input |
| :---------------: | :--: | :-------------: | :-------: | :-----: |
| Deol-Format | 00 | ld (lodeu dan-eo) | c (chugahada) | 10 |
| Deol-Format | 00 | jd (jeojang dan-eo) | c (chugahada) | 10 |
| Deol-Format | 00 | lj (lodeu juso) | c (chugahada) | 10 |
| Chu-Format | 00 | geb (gat-eumyeon bungi) | t (deolda) | 10 |
| Chu-Format | 00 | geb (gat-eumyeon bungi) | t (deolda) | 10 |




