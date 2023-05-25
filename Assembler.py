import re

from math import pow

class Assembler:
    context = None
    program = ""

    insts = ["lj", "lw", "ld", "jd", "jc", "dl", "jci", "geb",
            "ggb","yibi", "migs", "yabi", "i", "d", "ia", "lda",
            "cmp", "cmpi"]

    chu_insts = ["lr", "jd", "jc", "dl", "i", "geu", "ton"]
    dtypes = [".word"]
    registers = ["$rm", *["$jn" + str(x) for x in range(0, 5+1)], "$jm", "$iu"]

    labelsAddress = {}
    RAMmemory = []

    DEC_REG=r"^[0-9]+$"
    HEX_REG=r"^0x[0-9A-Fa-f]+$"
    TAB_REG=r"\t+"

    def __init__(self) -> None:
        pass

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

        # new context definition
        if (line[0] == "."):
            new_ctx = line[1:]
            self.change_context(new_ctx)
        # read variables and its values
        elif (self.context == "data"):
            self.handle_data(line)
        # read instructions
        elif (self.context == "text"):
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
            
        data_addr = self.ram_size()
        
        self.labelsAddress[tokens[0][:-1]] = data_addr

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
            except:
                print("erro: ", tokens)
                exit(1)

    def save_inst(self, inst, arg1=None, arg2=None, arg3=None):
        if (inst in self.chu_insts):
            self.save_chu_inst(inst, arg1, arg2, arg3)

    def save_chu_inst(self, inst, r1, r2, immediate):
        opcode = self.get_opcode(inst)

        inst_word = opcode << 3
        inst_word += self.get_register(r1)
        inst_word = inst_word << 3
        inst_word += self.get_register(r2)
        inst_word = inst_word << 4
        inst_word += int(immediate if immediate else '0')
        
        first_part_inst = (inst_word & 0xFF00) >> 8
        second_part_inst = (inst_word & 0x00FF)

        self.save_value(first_part_inst)
        self.save_value(second_part_inst)

        print("Inst: ", inst, r1, r2, immediate, ">>",inst_word)


    def get_opcode(self, inst):
        return 0b111111
    
    def get_register(self, register):
        return 0b011
        
        
    def convert_data_to_memory(self, value, type):
        converted_value = self.convert_value(value, type)

        if (converted_value > pow(2, 15) - 1
            or converted_value < -pow(2, 15)):
            raise Exception(converted_value + " cant be represent in 16 bits")

        self.save_value(converted_value)

    def convert_value(self, value, type):
        if type == ".word":
            if re.match(self.DEC_REG, value):
                return int(value)
            elif re.match(self.HEX_REG, value):
                return int(value, base=16)
        return 0


    def change_context(self, new_ctx):
        self.context = new_ctx
        print("New Context >>", new_ctx)


    def save_value(self, value):
        self.RAMmemory.append((hex(value)[2:]).zfill(2))
    
    def ram_size(self):
        return len(self.RAMmemory)

if __name__ == "__main__":
    assembler = Assembler()
    assembler.execute("Bangtan.asm")
    print(assembler.labelsAddress)
    print(assembler.RAMmemory)