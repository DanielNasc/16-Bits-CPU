import re

from math import pow
    
class ROMMemory:
    labelsValues = {}
    ROMmemory = []
    hex_mem = []

    def save_label(self, label, value=None):
        if not value:
            value = self.size()
        
        self.labelsValues[label] = value

    def save(self, value):
        self.ROMmemory.append(value)
    
    def size(self):
        return len(self.ROMmemory)
    
    def get_label_index(self, label):
        return self.labelsValues[label]

    def convert_labels(self):
        for word_arr in self.ROMmemory:
            word = word_arr[0]
            if len(word_arr) > 1:
                print(word_arr)
                label_addr = self.get_label_index(word_arr[1])
                label_addr = label_addr << 1
                word += label_addr
            self.hex_mem.append((hex(word)[2:]).zfill(4))

    def save_ROM_content(self, file):
        f = open(file, "w")
        f.write("v2.0 raw\n")
        for word in self.hex_mem:
            f.write(word + " ")
        f.close()


class Assembler:
    section = None

    ROM=None

    chu_insts = ["lr", "llj", "jd", "ld", "jc", "dl", "i", "geu", "ton", "aton"]
    deol_insts= ["lj", "ia", "dli", "ldi" "la", "jci", "dli", "ja", "dli", "dr", "cmp", "yibi", "yabi",]
    jeon_insts= ["lja", "kk", "lad", "lal","lj0", "lj1", "sal", "sj0", "sj1", "ldj0", "jai", "g","geb", "d", "dal", "cmpi", "lda", "end"]
    insts     = chu_insts + deol_insts + jeon_insts

    OPCODES = {
    "lja": 0b000001,
    "sal": 0b000010,
    "lal": 0b000011,
    "llj": 0b000100,
    "sj0": 0b000101,
    "jci": 0b000110,
    "lj0": 0b000111,
    "yabi": 0b001000,
    "lj1": 0b001001,
    "kk": 0b001010,
    "cmp": 0b001011,
    "geb": 0b001100,
    "dli": 0b001101,
    "d": 0b001110,
    "end": 0b001111
}
    dtypes = [".word"]
    registers = ["$zero", "$iu", "$jn0", "$jn1", "$sp", "$ps", "$bj", "$bb"]

    DEC_REG=r"^[0-9]+$"
    HEX_REG=r"^0x[0-9A-Fa-f]+$"
    TAB_REG=r"\t+"

    def __init__(self) -> None:
        self.ROM = ROMMemory()

    def execute(self, file):
        f = open(file, "r")
        print(self.registers)

        for line in f:
            self.handle_line(line)

        f.close()

        print(self.ROM.labelsValues)
        # print(self.ROM.)

        self.ROM.convert_labels()

        self.ROM.save_ROM_content("out.mem")

    def handle_line(self, line):
        line = line.strip()

        if (len(line) == 0): 
            return

        # new section definition
        if (line[0] == "."):
            new_ctx = line[1:]
            self.change_section(new_ctx)
        # read variables and its values
        elif (self.section == "data"):
            self.handle_data(line)
        # read instructions
        elif (self.section == "text"):
            self.handle_insts(line)
        elif (self.section == "vars"):
            self.handle_vars(line)
    
    def handle_data(self, line):
        tokens = line.split(" ")

        if (len(tokens) < 3 
            or tokens[0][len(tokens[0]) - 1] != ":"
            or tokens[1] not in self.dtypes
        ):
            raise Exception("Wrong syntax: ", tokens)
        
        values = tokens[2:]
    
        for value in values:
            if (not self.check_type(value, tokens[1])):
                raise Exception("wrong type \"" + value + "\" in " + str(tokens) + " not " + tokens[1])
            
        self.ROM.save_label(tokens[0][:-1])

        for token in tokens[2:]:
            self.convert_data_to_memory(token, tokens[1])
    
    def check_type(self, value, type):
        if (type == ".word"):
            return (re.match(self.DEC_REG, value)
                    or re.match(self.HEX_REG, value)# hexadecimal
                )

        return False
    
    def handle_vars(self, line):
        line = re.sub(self.TAB_REG, " ", line)
        tokens = list(filter(None, line.split(" ")))
        
        if len(tokens) != 3 or tokens[1] != "=" or not self.check_type(tokens[2], ".word"):
            raise Exception("Correct syntax:: [Var name] = [Hex|Dec Value]")
        
        self.ROM.save_label(tokens[0], self.convert_data_to_memory(tokens[2], ".word"))
        

    def handle_insts(self, line):
        line = re.sub(self.TAB_REG, " ", line)
        tokens = list(filter(None, line.split(" ")))
        is_label = tokens[0][len(tokens[0]) - 1] == ":"

        if ((not is_label and tokens[0] not in self.insts)):
            raise Exception("Wrong syntax:: inst " + str(tokens[0]) )
        
        if (is_label):
            self.ROM.save_label(tokens[0][:-1])
        else:
            try:
                self.save_inst(*tokens)
            except Exception as e:
                print("erro: ", tokens)
                print("msg: ", str(e))
                exit(1)

    def save_inst(self, inst, arg1=None, arg2=None, arg3=None):
        if (inst in self.chu_insts):
            self.save_chu_inst(inst, arg1, arg2, arg3)
        elif (inst in self.deol_insts):
            
            self.save_deol_inst(inst, arg1, arg2)
        elif (inst in self.jeon_insts):
            self.save_jeon_inst(inst, arg1)

    def save_chu_inst(self, inst, r1, r2, immediate):
        opcode = self.get_opcode(inst)

        inst_word = opcode << 3
        inst_word += self.get_register(r1)
        inst_word = inst_word << 3
        inst_word += self.get_register(r2)
        inst_word = inst_word << 4
        inst_word += int(immediate if immediate else '0')

        self.ROM.save([inst_word])
        
        # first_part_inst = (inst_word & 0xFF00) >> 8
        # second_part_inst = (inst_word & 0x00FF)

        # self.ROM.save(first_part_inst)
        # self.ROM.save(second_part_inst)

        print("Chu-Inst: ", inst, r1, r2, immediate, ">>", bin(inst_word))

    def save_deol_inst(self, inst, r1, immediate):
        if immediate == None: 
            immediate = '0'

        opcode = self.get_opcode(inst)

        inst_word = opcode << 3
        inst_word += self.get_register(r1)
        inst_word = inst_word << 7
        inst_word += self.convert_value(immediate, ".word")

        self.ROM.save([inst_word])

        print("Deol-Inst: ", inst, r1, immediate, ">>", bin(inst_word))

    def save_jeon_inst(self, inst, immediate: str):
        opcode = self.get_opcode(inst)

        inst_word = opcode << 10
        if immediate != None:
            if immediate.isnumeric():
                inst_word += int(immediate)
                self.ROM.save([inst_word])
            else:
                self.ROM.save([inst_word, immediate])
        else:
            self.ROM.save([inst_word])

        print("Jeon-Inst: ", inst, immediate, ">>", bin(inst_word))

    def get_opcode(self, inst):
        return self.OPCODES[inst]
    
    def get_register(self, register):
        try:
            return self.registers.index(register)
        except ValueError:
            print("Registrador não existente: " + register)
            exit(1)
        
    def convert_data_to_memory(self, value, type):
        converted_value = self.convert_value(value, type)

        if (converted_value > pow(2, 15) - 1
            or converted_value < -pow(2, 15)):
            raise Exception(converted_value + " cant be represent in 16 bits")

        self.ROM.save([converted_value])

    def convert_value(self, value, type):
        if type == ".word":
            if re.match(self.DEC_REG, value):
                return int(value)
            elif re.match(self.HEX_REG, value):
                return int(value, base=16)
        return 0

    def change_section(self, new_ctx):
        self.section = new_ctx
        print("New section >>", new_ctx)

if __name__ == "__main__":
    assembler = Assembler()
    assembler.execute("Bangtan.asm")
    print(assembler.ROM.ROMmemory)
    # print(assembler.ROM.hex_mem)
    for word in assembler.ROM.hex_mem:
        print(bin(int(word, 16))[2:].zfill(8))
        print(word)