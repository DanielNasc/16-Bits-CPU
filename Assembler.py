import re

from math import pow
    
class MemManager:
    labelsValues = {}
    RAMmemory = []
    ROMmemory = []
    hex_ram_mem = []
    hex_rom_mem = []
    variables = []

    def save_label(self, label, value=None, src="RAM"):
        if not value:
            value = self.size(src)
        
        self.labelsValues[label] = value

    def save_variable(self, label, value):
        self.variables.append(label)
        self.save_label(label, value)

    def save(self, value, dest):
        if dest == "RAM":
            self.RAMmemory.append(value)
        elif dest == "ROM":
            self.ROMmemory.append(value)
    
    def size(self, m):
        if m == "RAM":
            return len(self.RAMmemory)
        elif m == "ROM":
            return len(self.ROMmemory)

        return -1
    
    def get_label_index(self, label):
        return self.labelsValues[label]

    def convert_labels(self):
        for word_arr in self.ROMmemory:
            word = word_arr[0]
            if len(word_arr) > 1:
                label_addr = self.get_label_index(word_arr[1])
                # label_addr = label_addr << 1
                word += label_addr
                if word_arr[1] in self.variables:
                    # set most significant bit to 1
                    word = word | 0b1000000000000000
            self.hex_rom_mem.append((hex(word)[2:]).zfill(4))
 
    def save_ROM_content(self, file):
        f = open(file, "w")
        f.write("v2.0 raw\n")
        for word in self.hex_rom_mem:
            f.write(word + " ")
        f.close()


class Assembler:
    section = None

    MM=None

    chu_insts = ["slt", "ton", ]
    deol_insts= ["toni", "ld", "dli", "jci"]
    jeon_insts= ["d"]
    insts     = chu_insts + deol_insts + jeon_insts

    OPCODES = {
    "ld  ": 0b0000,
    "yibi": 0b0001,
    "yabi": 0b0010,
    "slt": 0b0011,
    "ton": 0b0100,
    "jci": 0b0101,
    "dli": 0b0110,
    "jc": 0b0111,   
    "d": 0b1000,
    }

    dtypes = [".word"]
    registers = ["$zero", "jn0", "$jn1", "$jn2", "$jn3", "$sg0", "$sg1", "$sg2", "$sg3", "$sg4", "$sg5"
                "$gp", "$sp", "$pp", "$bj", "$bb"]
    init_addr = 0

    DEC_REG=r"^[0-9]+$"
    HEX_REG=r"^0x[0-9A-Fa-f]+$"
    TAB_REG=r"\t+"

    def __init__(self) -> None:
        self.MM = MemManager()

    def execute(self, file):
        f = open(file, "r")
        print(self.registers)

        for line in f:
            self.handle_line(line)

        f.close()

        print(self.MM.labelsValues)
        # print(self.MM.)

        self.MM.convert_labels()

        self.MM.save_ROM_content("out.mem")

    def handle_line(self, line):
        line = line.strip()
        line = re.sub(self.TAB_REG, " ", line)
        tokens = list(filter(None, line.split(" ")))

        if (len(line) == 0 or len(tokens) == 0): 
            return
        
        # new section definition
        if (line[0] == "."):
            new_ctx = line[1:]
            self.change_section(new_ctx)
            return 

        # read variables and its values
        if (self.section == "data"):
            self.handle_data(tokens)
        # read instructions
        elif (self.section == "text"):
            self.handle_insts(tokens)
    
    def handle_data(self, tokens):
        if (len(tokens) < 3 
            or tokens[0][len(tokens[0]) - 1] != ":"
            or tokens[1] not in self.dtypes
        ):
            raise Exception("Wrong syntax: ", tokens)
        
        values = tokens[2:]
    
        for value in values:
            if (not self.check_type(value, tokens[1])):
                raise Exception("wrong type \"" + value + "\" in " + str(tokens) + " not " + tokens[1])
            
        self.MM.save_label(tokens[0][:-1], src="RAM")

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
        
        self.MM.save_variable(tokens[0], self.convert_value(tokens[2], ".word"))
        

    def handle_insts(self, tokens):
        is_label = tokens[0][len(tokens[0]) - 1] == ":"

        if ((not is_label and tokens[0] not in self.insts)):
            raise Exception("Wrong syntax:: inst " + str(tokens[0]) )
        
        if (is_label):
            self.MM.save_label(tokens[0][:-1], src="ROM")
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

        self.MM.save([inst_word], "ROM")
        
        # first_part_inst = (inst_word & 0xFF00) >> 8
        # second_part_inst = (inst_word & 0x00FF)

        # self.MM.save(first_part_inst)
        # self.MM.save(second_part_inst)

        print("Chu-Inst: ", inst, r1, r2, immediate, ">>", bin(inst_word))

    def save_deol_inst(self, inst, r1, immediate):
        if immediate == None: 
            immediate = '0'

        opcode = self.get_opcode(inst)

        inst_word = opcode << 3
        inst_word += self.get_register(r1)
        inst_word = inst_word << 7
        try:
            inst_word += self.convert_value(immediate, ".word")

            self.MM.save([inst_word], "ROM")
        except:
            self.MM.save([inst_word, immediate], "ROM")

        print("Deol-Inst: ", inst, r1, immediate, ">>", bin(inst_word))

    def save_jeon_inst(self, inst, immediate: str):
        opcode = self.get_opcode(inst)

        inst_word = opcode << 10
        if immediate != None:
            if immediate.isnumeric():
                inst_word += int(immediate)
                self.MM.save([inst_word], "ROM")
            else:
                self.MM.save([inst_word, immediate], "ROM")
        else:
            self.MM.save([inst_word], "ROM")

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

        self.MM.save([converted_value], "RAM")

    def convert_value(self, value, type):
        if type == ".word":
            if re.match(self.DEC_REG, value):
                return int(value)
            elif re.match(self.HEX_REG, value):
                return int(value, base=16)
        raise Exception("Invalid type and/or value: ")

    def change_section(self, new_ctx):
        self.section = new_ctx
        print("New section >>", new_ctx)

        # JUMP TO INIT ADDR: ignore data section in rom

        # if self.section == "data":
        #     self.MM.save([self.OPCODES["d"] << 10, "__init_addr__"]) # j __init_addr__
        # elif self.section == "text":
        #     self.MM.save_label("__init_addr__", self.init_addr) # init_addr = first instruction in text section
        # else:
        #     self.init_addr = self.MM.size() # first instruction in data section


if __name__ == "__main__":
    assembler = Assembler()
    assembler.execute("Bangtan.asm")
    print(assembler.MM.variables)
    print(assembler.MM.ROMmemory)
    print(assembler.MM.RAMmemory)
    # print(assembler.ROM.hex_rom_mem)
    for word in assembler.MM.hex_rom_mem:
        print(bin(int(word, 16))[2:].zfill(16))
        print(word)