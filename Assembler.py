import re

from math import pow

OPCODES ={
    "lj": 0b1, 
    "lw": 0,
    "ld": 0,
    "jd": 0,
    "jc": 0,
    "dl": 0,
    "jci": 0,
    "geb": 0,
    "ggb": 0,
    "yibi": 0,
    "migs": 0,
    "yabi": 0,
    "i": 0,
    "d": 0,
    "ia": 0,
    "lda": 0,
    "cmp": 0,
    "cmpi": 0
}

class RamMemory:
    labelsAddress = {}
    RAMmemory = []

    def save_label(self, label):
        data_addr = self.size()
        
        self.labelsAddress[label] = data_addr

    def save(self, value):
        # self.RAMmemory.append((hex(value)[2:]).zfill(2))
        self.RAMmemory.append(value)
    
    def size(self):
        return len(self.RAMmemory)
    
    def get_label_index(self, label):
        return self.labelsAddress[label]

    def convert_labels(self):
        pass

class Assembler:
    section = None
    program = ""

    RAM=None

    chu_insts = ["lr", "jd", "jc", "dl", "i", "geu", "ton", "aton"]
    deol_insts= ["lj", "ia", "ld", "ldi" "la", "jci", "dli", "ja", "dli", "dr", "cmp"]
    jeon_insts= ["lja", "lda", "jai", "g","geb", "yibi", "yabi", "d", "dal", "cmpi"]
    insts     = chu_insts + deol_insts + jeon_insts
    
    dtypes = [".word"]
    registers = ["$rm", *["$jn" + str(x) for x in range(0, 5+1)], "$jm", "$iu"]

    DEC_REG=r"^[0-9]+$"
    HEX_REG=r"^0x[0-9A-Fa-f]+$"
    TAB_REG=r"\t+"

    def __init__(self) -> None:
        self.RAM = RamMemory()

    def execute(self, file):
        f = open(file, "r")
        print(self.registers)

        for line in f:
            self.handle_line(line)

        f.close()

        mem_file = open("outRAM.mem", "w")


        mem_file.close()

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
            
        self.RAM.save_label(tokens[0][:-1])

        for token in tokens[2:]:
            self.convert_data_to_memory(token, tokens[1])
    
    def check_type(self, value, type):
        if (type == ".word"):
            return (re.match(self.DEC_REG, value)
                    or re.match(self.HEX_REG, value)# hexadecimal
                )

        return True

    def handle_insts(self, line):
        line = re.sub(self.TAB_REG, " ", line)
        tokens = list(filter(None, line.split(" ")))
        is_label = tokens[0][len(tokens[0]) - 1] == ":"

        if ((not is_label and tokens[0] not in self.insts)):
            raise Exception("Wrong syntax:: inst " + str(tokens[0]) )
        
        if (not is_label):
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
            self.save_deol_inst(inst, arg1)
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

        self.RAM.save([inst_word])
        
        # first_part_inst = (inst_word & 0xFF00) >> 8
        # second_part_inst = (inst_word & 0x00FF)

        # self.RAM.save(first_part_inst)
        # self.RAM.save(second_part_inst)

        print("Chu-Inst: ", inst, r1, r2, immediate, ">>", inst_word)

    def save_deol_inst(self, inst, immediate_r1):
        opcode = self.get_opcode(inst)

        inst_word = opcode << 3
        
        immediate_r1 = immediate_r1.split("(")
        immediate = immediate_r1[0]
        # immediate($register) || $register
        if len(immediate_r1) > 1:r1 = immediate_r1[1][:-1] 
        else: 
            r1 =immediate_r1[0]
            immediate = '0'

        inst_word += self.get_register(r1)
        inst_word = inst_word << 7
        inst_word += self.convert_value(immediate, ".word")

        self.RAM.save([inst_word])

        print("Deol-Inst: ", inst, r1, immediate, ">>", inst_word)

    def save_jeon_inst(self, inst, immediate: str):
        opcode = self.get_opcode(inst)

        inst_word = opcode << 10
        if immediate.isnumeric():
            inst_word += int(immediate)
            self.RAM.save([inst_word])
        else:
            self.RAM.save([inst_word, immediate])
            # label_i = self.RAM.get_label_index(immediate)
            # inst_word += (label_i << 1)

        # first_part_inst = (inst_word & 0xFF00) >> 8
        # second_part_inst = (inst_word & 0x00FF)

        # self.RAM.save(first_part_inst)
        # self.RAM.save(second_part_inst)


        print("Jeon-Inst: ", inst, immediate, ">>", inst_word)

    def get_opcode(self, inst):
        return 0b111111
    
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

        self.RAM.save([converted_value])

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
    print(assembler.RAM.labelsAddress)
    print(assembler.RAM.RAMmemory)
    # for byte in assembler.RAM.RAMmemory:
        # print(bin(int(byte, 16)).zfill(8))
        # print(byte)