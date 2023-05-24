class Assembler:
    context = None
    program = ""

    ints = ["lj," "lw", "ld", "jd", "jc", "dl", "jci", "geb",
            "ggb","yibi", "migs", "yabi", "i", "d"]
    dtypes = ["word"]

    varMetadata = {}
    RAMmemory = []

    def __init__(self) -> None:
        pass

    def execute(self, file):
        f = open(file, "r")

        for line in f:
            self.handle_line(line)

        f.close()

        mem_file = open("outRAM.mem", "w")


        mem_file.close()

    def handle_line(self, line):
        line = line.strip()
        if (len(line) == 0): return

        # new context definition
        if (line[0] == "."):
            new_ctx = line[1:]
            self.change_context(new_ctx)
        # read variables and its values
        elif (self.context == "data"):
            self.handle_data(line)
        # read instructions
        elif (self.context == "inst"):
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

    
    def check_type(self, value, type):
        try:
            if (type == "word"):
                int(value)
            return True
        except ValueError:
            return False


    def handle_insts(self, line):
        tokens = line.split(" ")

        if (len(tokens) < 2
            or (tokens[0][0] != "." and tokens[0] not in self.ints)
        ):
            raise Exception("Wrong syntax:: inst")
        

    def change_context(self, new_ctx):
        self.context = new_ctx
        print("New Context >>", new_ctx)


if __name__ == "__main__":
    assembler = Assembler()
    assembler.execute("Bangtan.asm")