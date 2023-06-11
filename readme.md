# Processador Bangtan

#### Formato das Instruções
| Tipo de Instrução | OpCode | Registradores | Imediato |
| :---------------: | :----: | :-----------: | :------: |
| Chu-Format | 4 bits | 12 bits | - |
| Deol-Format | 4 bits | 8 bits | 4 bits |
| Hobi-Format | 4 bits | 4 bits | 8 bits |
| Jeon-Format | 4 bits | - | 12 bits |

### Registradores
16 registradores
Os registradores são procedidos de $ nas instruções
Duas formas de representação:
Numero do registrador. $0 até $15
Usando os nomes equivalentes (ver abaixo)
| # do Reg. | Nome | Descrição |
| :-------: | :--: | :-------: |
| 0 | $zero | Sempre 0 |
| 1 | $t0 | Temporário 0 |
| 2 | $t1 | Temporário 1 |
| 3 | $t2 | Temporário 2 |
| 4 | $t3 | Temporário 3 |
| 5 | $s0 | Salvo 0 |
| 6 | $s1 | Salvo 1 |
| 7 | $s2 | Salvo 2 |
| 8 | $s3 | Salvo 3 |
| 9 | $s4 | Salvo 4 |
| 10 | $s5 | Salvo 5 |
| 11 | $gp | Ponteiro Global |
| 12 | $sp | Ponteiro de Pilha |
| 13 | $fp | Ponteiro de Frame |
| 14 | $ra | Endereço de Retorno |


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
| **lw** (load word) | **ld** | lodeu dan-eo"
| **sw** (store word)| **jd** | jeojang dan-eo
| **add** | **jc** | jeugsi chuga
| **addi** | **jci** | -
| **sub** | **dl** | deolda
| **subi** | **dli** | -
| **j** (jump) | **d** | doyag
| **and** | **geu** | geuligo
| **andi** | **geui** | -
| **or** | **ton** | ttoneun
| **ori** | **toni** | -
| **nor** | **aton** | -
| **xor** | **xton** | -
| **beq** (branch if equal) | **jge** | jeongdang geuligo
| **slt** (set less than) | **jg** | jeongdang geuligo

### Leitura/Escrita
Acesso a memória RAM apenas com instruções de leitura e escrita.
Todas outras instruções usam registradores como operando.

#### Leitura/Escrita de Dados
##### Leitura:
- `ld registrador1 registrador2 offset`

copia word(2 bytes) da posição da RAM dada pelo registrador2 somado ao offset, para o registrador1.

##### Escrita:
- `jd registrador1 endereço`

copia word(2 bytes) do registrador1 para a posição da RAM dada pelo endereço.

### Instruções Aritméticas
#### Instruções Aritméticas
- `jc registrador1 registrador2 registrador3`

soma o conteúdo dos registradores registrador2 e registrador3 e guarda o resultado no registrador1.

- `jci registrador1 registrador2 imediato`

soma o conteúdo do registrador registrador2 com o imediato e guarda o resultado no registrador1.

- `dl registrador1 registrador2 registrador3`

subtrai o conteúdo dos registradores registrador2 e registrador3 e guarda o resultado no registrador1.

- `dli registrador1 registrador2 imediato`

subtrai o conteúdo do registrador registrador2 com o imediato e guarda o resultado no registrador1.

#### Instruções Lógicas

- `geu registrador1 registrador2 registrador3`

faz a operação lógica AND entre os registradores registrador2 e registrador3 e guarda o resultado no registrador1.

- `geui registrador1 registrador2 imediato`

faz a operação lógica AND entre o registrador registrador2 e o imediato e guarda o resultado no registrador1.

- `ton registrador1 registrador2 registrador3`

faz a operação lógica OR entre os registradores registrador2 e registrador3 e guarda o resultado no registrador1.

- `toni registrador1 registrador2 imediato`

faz a operação lógica OR entre o registrador registrador2 e o imediato e guarda o resultado no registrador1.

- `aton registrador1 registrador2 registrador3`

faz a operação lógica NOR entre os registradores registrador2 e registrador3 e guarda o resultado no registrador1.

- `xton registrador1 registrador2 registrador3`

faz a operação lógica XOR entre os registradores registrador2 e registrador3 e guarda o resultado no registrador1.

#### Instruções de Desvio

- `d endereço`

desvia para o endereço dado.

- `jge registrador1 registrador2 endereço`

desvia para o endereço dado se o conteúdo dos registradores registrador1 e registrador2 forem iguais.

#### Instrução de Comparação

- `jg registrador1 registrador2`

compara o conteúdo dos registradores registrador1 e registrador2 e guarda 1 no registrador1 se o conteúdo do registrador1 for menor que o do registrador2, caso contrário guarda 0.

### Tabela de Opcodes e Sinais de Controle

|Instruction|Type|Opcode|RegDest|Branch|MemRead|MemToReg|ALUOp|MemWrite|ALUSrc|RegWrite|jump|
|-----------|----|------|-------|------|-------|--------|-----|--------|------|--------|----|
|add        |chu |0b0000|1      |0     |0      |0       |11   |0       |0     |1       |0   |
|sub        |chu |0b0001|1      |0     |0      |0       |100  |0       |0     |1       |0   |
|and        |chu |0b0010|1      |0     |0      |0       |0    |0       |0     |1       |0   |
|or         |chu |0b0011|1      |0     |0      |0       |1    |0       |0     |1       |0   |
|nor        |chu |0b0100|1      |0     |0      |0       |0   |0       |0     |1       |0   |
|xor        |chu |0b1110|1      |0     |0      |0       |11   |0       |0     |1       |0   |
|lw         |deol|0b0101|0      |0     |1      |1       |11   |0       |1     |1       |0   |
|sw         |deol|0b0110|x      |0     |0      |0       |11   |1       |1     |0       |0   |
|beq        |deol|0b0111|x      |1     |0      |0       |100  |0       |0     |0       |0   |
|slt        |chu |0b1000|1      |0     |0      |0       |101  |0       |0     |1       |0   |
|addi       |deol|0b1001|0      |0     |0      |0       |11   |0       |1     |1       |0   |
|subi       |deol|0b1010|0      |0     |0      |0       |100  |0       |1     |1       |0   |
|ori        |deol|0b1011|0      |0     |0      |0       |1    |0       |1     |1       |0   |
|sll        |deol|0b1100|0      |0     |0      |0       |     |        |      |        |    |
|srl        |deol|0b1101|0      |0     |0      |0       |     |        |      |        |    |
|j          |jeon|0b1111|x      |0     |0      |0       |11   |0       |x     |0       |1   |
