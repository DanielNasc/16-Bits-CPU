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

### Instruções MIPS >> Bangtan
| Nome da Instrução (MIPS) | Nome da Instrução (Bangtan) |
| :----------------------: | :-------------------------: |
| **la** (load address) | **lj** (lodeu juso)
| **lw** (load word) | **ld** (lodeu dan-eo)
| **sw** | **jd** (jeojang dan-eo)|
| **add** | **jc** (Chugahada) |
| **sub** | **dl** (Deolda) |
| **addi** | **jci** (Jeugsi chuga) |
| **beq** | **geb** (Gat-eumyeon bungi) |
| **bcc** | **ggb** (Kaeli keullin bungi) |
| **beqz** | **yibi** (Yeong imyeon bungi) |
| **slt** | **migs** (Miman-in gyeong-u seoljeong) |
| **bnez** | **yabi** (Yeongi anin gyeong-u bungi) |
| **move** | **i** (idonghada) |
| **j** | **d** (doyag) |

### Leitura/Escrita
Acesso a memória RAM apenas com instruções de leitura e escrita.
Todas outras instruções usam registradores como operando.

##### Leitura/Escrita de endereçamento direto
**Leitura:**
- **ld** registrador, posição_da_RAM
copia word(2 bytes) da posição da RAM dada, para o registrador dado.

### Controle da ALU
| Instruction Opcode | ALUOp | Instruction Operation | Desired ALU Action | ALU Control Input |
| :---------------: | :--: | :-------------: | :-------: | :-----: |
| Deol-Format | 00 | ld (lodeu dan-eo) | c (chugahada) | 10 |
| Deol-Format | 00 | jd (jeojang dan-eo) | c (chugahada) | 10 |
| Deol-Format | 00 | lj (lodeu juso) | c (chugahada) | 10 |
| Chu-Format | 00 | geb (gat-eumyeon bungi) | t (deolda) | 10 |
| Chu-Format | 00 | geb (gat-eumyeon bungi) | t (deolda) | 10 |




