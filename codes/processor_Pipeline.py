import time
def sign_Extend(imm):
    immediate = None
    if imm[0] == '1':
        immediate = "1111111111111111" + imm
        return immediate
    else:
        immediate = "0000000000000000" + imm
        return immediate

def jump_Extend(jump_Address):
    return "00" + jump_Address + "0000"

instr_mem = {}
data_mem = {}
for i in range(101):
    data_mem[i] = 0
data_mem[4] = 4
data_mem[8] = 4
reg_mem = {
    "00000": 0,
    "00001": 0,
    "00010": 0,
    "00011": 0,
    "00100": 0,
    "00101": 0,
    "00110": 0,
    "00111": 0,
    "01000": 0,
    "01001": 0,
    "01010": 0,
    "01011": 0,
    "01100": 0,
    "01101": 0,
    "01110": 0,
    "01111": 0,
    "10000": 0,
    "10001": 0,
    "10010": 0,
    "10011": 0,
    "10100": 0,
    "10101": 0,
    "10110": 0,
    "10111": 0,
    "11000": 0,
    "11001": 0,
    "11010": 0,
    "11011": 0,
    "11100": 0,
    "11101": 0,
    "11110": 0,
    "11111": 0,
}
function_Mem = {
    "100000": "add",
    "100100": "and",
    "100101": "or",
    "101010": "slt",
    "100010": "subtract",
    "100001" : "addu",
    "000000" : "sll"
}
opcode = {
    "000000": "R",
    "001000": "addi",
    "000100": "beq",
    "000010": "j",
    "000011": "jal",
    "100011": "load",
    "101011": "store",
    "000101": "bne",
}
stages = {
    0 : "FETCH",
    1 : "DECODE",
    2 : "EXECUTE",
    3 : "MEMORY",
    4 : "WRITE BACK"
}

kundali = {}
dependency_Dict = {}

class Instruction:
    def decode(self, instruction, program_Counter):
        # R format
        if instruction[0:6] == "000000":
            regdst = True
            Branch = False
            Mem_read = False
            Mem_to_reg = False
            Mem_wri = False
            RegWr = True
            jump = False
            ALU_src = False
            jump_And_Link = True
            if regdst:
                reg_Dest = instruction[16:21]
            else:
                reg_Dest = instruction[11:16]
            decode_Dict = {
                "opcode": opcode[instruction[0:6]],
                "reg_src_1": reg_mem[instruction[6:11]],
                "reg_src_2": reg_mem[instruction[11:16]],
                "reg_src_1_address" : instruction[6:11],
                "reg_src_2_address" : instruction[11:16],
                "reg_dest": reg_Dest,
                "function": function_Mem[instruction[26:32]],
                "regdst": regdst,
                "Branch": Branch,
                "Mem_read": Mem_read,
                "Mem_to_reg": Mem_to_reg,
                "Mem_wri": Mem_wri,
                "RegWr": RegWr,
                "jump": jump,
                "ALU_src": ALU_src,
                "jump_And_Link" : jump_And_Link,
                "shamt" : instruction[21:26]
            }
            return decode_Dict
        # addi
        if instruction[0:6] == "001000":
            regdst = False
            Branch = False
            Mem_read = False
            Mem_to_reg = False
            ALU_src = True
            Mem_wri = False
            RegWr = True
            jump = False
            jump_And_Link = True
            if regdst:
                reg_Dest = instruction[16:21]
            else:
                reg_Dest = instruction[11:16]
            decode_Dict = {
                "opcode": opcode[instruction[0:6]],
                "reg_src_1": reg_mem[instruction[6:11]],
                "reg_src_1_address" : instruction[6:11],
                "reg_src_2": reg_Dest,
                "immediate": sign_Extend(instruction[16:32]),
                "regdst": regdst,
                "Branch": Branch,
                "Mem_read": Mem_read,
                "Mem_to_reg": Mem_to_reg,
                "Mem_wri": Mem_wri,
                "RegWr": RegWr,
                "jump": jump,
                "ALU_src": ALU_src,
                "jump_And_Link" : jump_And_Link
            }
            return decode_Dict
        # load
        if instruction[0:6] == "100011":
            regdst = False
            Branch = False
            Mem_read = True
            Mem_to_reg = True
            ALU_src = True
            Mem_wri = False
            RegWr = False
            jump = False
            jump_And_Link = True
            if regdst:
                reg_Dest = instruction[16:21]
            else:
                reg_Dest = instruction[11:16]
            decode_Dict = {
                "opcode": opcode[instruction[0:6]],
                "reg_src_1": reg_mem[instruction[6:11]],
                "reg_src_1_address" : instruction[6:11],
                "reg_dest": reg_Dest,
                "immediate": sign_Extend(instruction[16:32]),
                "regdst": regdst,
                "Branch": Branch,
                "Mem_read": Mem_read,
                "Mem_to_reg": Mem_to_reg,
                "Mem_wri": Mem_wri,
                "RegWr": RegWr,
                "jump": jump,
                "ALU_src": ALU_src,
                "jump_And_Link" : jump_And_Link
            }
            return decode_Dict
        # store
        if instruction[0:6] == "101011":
            regdst = None
            Branch = False
            Mem_read = False
            Mem_to_reg = False
            ALU_src = True
            Mem_wri = True
            RegWr = False
            jump = False
            jump_And_Link = True
            decode_Dict = {
                "opcode": opcode[instruction[0:6]],
                "reg_src_1": reg_mem[instruction[6:11]],
                "reg_src_1_address" : instruction[6:11],
                "reg_src_2": reg_mem[instruction[11:16]],
                "reg_src_2_address" : instruction[11:16],
                "immediate": sign_Extend(instruction[16:32]),
                "regdst": regdst,
                "Branch": Branch,
                "Mem_read": Mem_read,
                "Mem_to_reg": Mem_to_reg,
                "Mem_wri": Mem_wri,
                "RegWr": RegWr,
                "jump": jump,
                "ALU_src": ALU_src,
                "jump_And_Link" : jump_And_Link
            }
            return decode_Dict
        # beq
        if instruction[0:6] == "000100":
            regdst = None
            Mem_read = False
            Mem_to_reg = False
            ALU_src = False
            Mem_wri = False
            RegWr = False
            jump = False
            jump_And_Link = False
            Branch = True
            decode_Dict = {
                "opcode": opcode[instruction[0:6]],
                "reg_src_1": reg_mem[instruction[6:11]],
                "reg_src_1_address" : instruction[6:11],
                "reg_src_2": reg_mem[instruction[11:16]],
                "reg_src_2_address" : instruction[11:16],
                "offset": sign_Extend(instruction[16:32]),
                "regdst": regdst,
                "Branch": Branch,
                "Mem_read": Mem_read,
                "Mem_to_reg": Mem_to_reg,
                "Mem_wri": Mem_wri,
                "RegWr": RegWr,
                "jump": jump,
                "ALU_src": ALU_src,
                "jump_And_Link" : jump_And_Link
            }
            return decode_Dict
        # jump
        if instruction[0:6] == "000010":
            regdst = None
            Branch = False
            Mem_read = False
            Mem_to_reg = False
            ALU_src = False
            Mem_wri = False
            RegWr = False
            jump = True
            jump_And_Link = False
            decode_Dict = {
                "opcode": opcode[instruction[0:6]],
                "jump_Address": jump_Extend(instruction[6:32]),
                "regdst": regdst,
                "Branch": Branch,
                "Mem_read": Mem_read,
                "Mem_to_reg": Mem_to_reg,
                "Mem_wri": Mem_wri,
                "RegWr": RegWr,
                "jump": jump,
                "ALU_src": ALU_src,
                "jump_And_Link" : jump_And_Link
            }
            return decode_Dict
        # bne
        if instruction[0:6] == "000101":
            regdst = None
            Mem_read = False
            Mem_to_reg = False
            ALU_src = False
            Mem_wri = False
            RegWr = False
            jump = False
            jump_And_Link = False
            Branch = True
            decode_Dict = {
                "opcode": opcode[instruction[0:6]],
                "reg_src_1": reg_mem[instruction[6:11]],
                "reg_src_1_address" : instruction[6:11],
                "reg_src_2": reg_mem[instruction[11:16]],
                "reg_src_2_address" : instruction[11:16],
                "offset": sign_Extend(instruction[16:32]),
                "regdst": regdst,
                "Branch": Branch,
                "Mem_read": Mem_read,
                "Mem_to_reg": Mem_to_reg,
                "Mem_wri": Mem_wri,
                "RegWr": RegWr,
                "jump": jump,
                "ALU_src": ALU_src,
                "jump_And_Link" : jump_And_Link
            }
            return decode_Dict
        # jal
        if instruction[0:6] == "000011":
            regdst = None
            # Branch = True
            Mem_read = False
            Mem_to_reg = False
            ALU_src = False
            Mem_wri = False
            RegWr = False
            jump = False
            jump_And_Link = True
            decode_Dict = {
                "opcode": opcode[instruction[0:6]],
                "jump_Address": jump_Extend(instruction[6:32]),
                "post_Execution_Address": program_Counter,
                "regdst": regdst,
                "Mem_read": Mem_read,
                "Mem_to_reg": Mem_to_reg,
                "Mem_wri": Mem_wri,
                "RegWr": RegWr,
                "jump": jump,
                "ALU_src": ALU_src,
                "jump_And_Link" : jump_And_Link
            }
            return decode_Dict
    def execute(self, decode_Dict, program_Counter):
        if decode_Dict["ALU_src"]:
            if(decode_Dict['immediate'][0] == '0'):
                ALU_Mux = int(decode_Dict['immediate'][17:32], 2)
            else:
                ALU_Mux = (1 << (len(decode_Dict['immediate'][16:32]) - 1)) - int(decode_Dict['immediate'][16:32], 2)
        elif(decode_Dict["ALU_src"] == False and decode_Dict['jump'] == False):
            ALU_Mux = decode_Dict["reg_src_2"]
        # R
        if decode_Dict["opcode"] == "R":
            reg_src_1_Value = decode_Dict["reg_src_1"]
            reg_src_2_Value = ALU_Mux
            # add
            if decode_Dict["function"] == "add" or decode_Dict["function"] == "addu":
                reg_dest_Value = reg_src_1_Value + reg_src_2_Value
                execute_Dict = {
                    "program_Counter" : None,
                    "reg_dest_Value": reg_dest_Value,
                    "reg_dest_Address": decode_Dict["reg_dest"],
                    "regdst": decode_Dict["regdst"],
                    "Branch": decode_Dict["Branch"],
                    "Mem_read": decode_Dict["Mem_read"],
                    "Mem_to_reg": decode_Dict["Mem_to_reg"],
                    "Mem_wri": decode_Dict["Mem_wri"],
                    "RegWr": decode_Dict["RegWr"],
                    "jump": decode_Dict["jump"],
                    "ALU_src": decode_Dict["ALU_src"],
                    "jump_And_Link" : decode_Dict["jump_And_Link"]
                }
                return execute_Dict
            # subtract
            if decode_Dict["function"] == "subtract":
                reg_dest_Value = reg_src_1_Value - reg_src_2_Value
                execute_Dict = {
                    "program_Counter" : None,
                    "reg_dest_Value": reg_dest_Value,
                    "reg_dest_Address": decode_Dict["reg_dest"],
                    "regdst": decode_Dict["regdst"],
                    "Branch": decode_Dict["Branch"],
                    "Mem_read": decode_Dict["Mem_read"],
                    "Mem_to_reg": decode_Dict["Mem_to_reg"],
                    "Mem_wri": decode_Dict["Mem_wri"],
                    "RegWr": decode_Dict["RegWr"],
                    "jump": decode_Dict["jump"],
                    "ALU_src": decode_Dict["ALU_src"],
                    "jump_And_Link" : decode_Dict["jump_And_Link"]
                }
                return execute_Dict
            # and
            if decode_Dict["function"] == "and":
                reg_dest_Value = reg_src_1_Value & reg_src_2_Value
                execute_Dict = {
                    "program_Counter" : None,
                    "reg_dest_Value": reg_dest_Value,
                    "reg_dest_Address": decode_Dict["reg_dest"],
                    "regdst": decode_Dict["regdst"],
                    "Branch": decode_Dict["Branch"],
                    "Mem_read": decode_Dict["Mem_read"],
                    "Mem_to_reg": decode_Dict["Mem_to_reg"],
                    "Mem_wri": decode_Dict["Mem_wri"],
                    "RegWr": decode_Dict["RegWr"],
                    "jump": decode_Dict["jump"],
                    "ALU_src": decode_Dict["ALU_src"],
                    "jump_And_Link" : decode_Dict["jump_And_Link"]
                }
                return execute_Dict
            # or
            if decode_Dict["function"] == "or":
                reg_dest_Value = reg_src_1_Value | reg_src_2_Value
                execute_Dict = {
                    "program_Counter" : None,
                    "reg_dest_Value": reg_dest_Value,
                    "reg_dest_Address": decode_Dict["reg_dest"],
                    "regdst": decode_Dict["regdst"],
                    "Branch": decode_Dict["Branch"],
                    "Mem_read": decode_Dict["Mem_read"],
                    "Mem_to_reg": decode_Dict["Mem_to_reg"],
                    "Mem_wri": decode_Dict["Mem_wri"],
                    "RegWr": decode_Dict["RegWr"],
                    "jump": decode_Dict["jump"],
                    "ALU_src": decode_Dict["ALU_src"],
                    "jump_And_Link" : decode_Dict["jump_And_Link"]
                }
                return execute_Dict
            # slt
            if decode_Dict["function"] == "slt":
                reg_dest_Value = reg_src_1_Value < reg_src_2_Value
                execute_Dict = {
                    "program_Counter" : None,
                    "reg_dest_Value": reg_dest_Value,
                    "reg_dest_Address": decode_Dict["reg_dest"],
                    "regdst": decode_Dict["regdst"],
                    "Branch": decode_Dict["Branch"],
                    "Mem_read": decode_Dict["Mem_read"],
                    "Mem_to_reg": decode_Dict["Mem_to_reg"],
                    "Mem_wri": decode_Dict["Mem_wri"],
                    "RegWr": decode_Dict["RegWr"],
                    "jump": decode_Dict["jump"],
                    "ALU_src": decode_Dict["ALU_src"],
                    "jump_And_Link" : decode_Dict["jump_And_Link"]
                }
                return execute_Dict
            # sll
            if decode_Dict["function"] == "sll":
                reg_dest_Value = reg_src_2_Value << int(decode_Dict['shamt'], 2)
                execute_Dict = {
                    "program_Counter" : None,
                    "reg_dest_Value": reg_dest_Value,
                    "reg_dest_Address": decode_Dict["reg_dest"],
                    "regdst": decode_Dict["regdst"],
                    "Branch": decode_Dict["Branch"],
                    "Mem_read": decode_Dict["Mem_read"],
                    "Mem_to_reg": decode_Dict["Mem_to_reg"],
                    "Mem_wri": decode_Dict["Mem_wri"],
                    "RegWr": decode_Dict["RegWr"],
                    "jump": decode_Dict["jump"],
                    "ALU_src": decode_Dict["ALU_src"],
                    "jump_And_Link" : decode_Dict["jump_And_Link"]
                }
                return execute_Dict
        # addi
        if decode_Dict["opcode"] == "addi":
            reg_src_1_Value = decode_Dict["reg_src_1"] 
            reg_dest_Address = decode_Dict["reg_src_2"] 
            immediate_value_Decimal = ALU_Mux 
            reg_dest_Value = reg_src_1_Value + immediate_value_Decimal
            execute_Dict = {
                "program_Counter" : None,
                "reg_dest_Value": reg_dest_Value,
                "reg_dest_Address": reg_dest_Address,
                "regdst": decode_Dict["regdst"],
                "Branch": decode_Dict["Branch"],
                "Mem_read": decode_Dict["Mem_read"],
                "Mem_to_reg": decode_Dict["Mem_to_reg"],
                "Mem_wri": decode_Dict["Mem_wri"],
                "RegWr": decode_Dict["RegWr"],
                "jump": decode_Dict["jump"],
                "ALU_src": decode_Dict["ALU_src"],
                "jump_And_Link" : decode_Dict["jump_And_Link"]
            }
            return execute_Dict
        # beq
        if decode_Dict["opcode"] == "beq":
            reg_src_1_Value = decode_Dict["reg_src_1"]
            reg_src_2_Value = ALU_Mux
            if(reg_src_1_Value == reg_src_2_Value):
                if(decode_Dict["offset"][0] == '0'):
                    program_Counter = program_Counter + 4 * int(decode_Dict["offset"][16:32], 2) + 4
                else:
                    binary_string = decode_Dict["offset"][16:32]
                    bit_length = len(binary_string)
                    program_Counter = program_Counter + 4 * (int(binary_string, 2) - (1 << bit_length)) + 4
            else:
                program_Counter = program_Counter + 4
            execute_Dict = {
                "program_Counter": program_Counter,
                "regdst": decode_Dict["regdst"],
                "Branch": decode_Dict['Branch'],
                "Mem_read": decode_Dict["Mem_read"],
                "Mem_to_reg": decode_Dict["Mem_to_reg"],
                "Mem_wri": decode_Dict["Mem_wri"],
                "RegWr": decode_Dict["RegWr"],
                "jump": decode_Dict["jump"],
                "ALU_src": decode_Dict["ALU_src"],
                "jump_And_Link" : decode_Dict["jump_And_Link"],
            }
            return execute_Dict
        # jump
        if decode_Dict["opcode"] == "j":
            program_Counter = int(decode_Dict["jump_Address"][4:30], 2)
            execute_Dict = {
                "program_Counter": program_Counter,
                "regdst": decode_Dict["regdst"],
                "Branch": decode_Dict["Branch"],
                "Mem_read": decode_Dict["Mem_read"],
                "Mem_to_reg": decode_Dict["Mem_to_reg"],
                "Mem_wri": decode_Dict["Mem_wri"],
                "RegWr": decode_Dict["RegWr"],
                "jump": decode_Dict["jump"],
                "ALU_src": decode_Dict["ALU_src"],
                "jump_And_Link" : decode_Dict["jump_And_Link"],
            }
            return execute_Dict
        # load
        if decode_Dict["opcode"] == "load":
            reg_src_1_Value = decode_Dict["reg_src_1"]
            immediate_value_Decimal = ALU_Mux
            reg_Dest_Address = decode_Dict["reg_dest"]
            value_To_Be_Stored = reg_src_1_Value + immediate_value_Decimal # 3
            execute_Dict = {
                "program_Counter" : None,
                "value_To_Be_Stored": value_To_Be_Stored,
                "reg_dest_Address": reg_Dest_Address,
                "regdst": decode_Dict["regdst"],
                "Branch": decode_Dict["Branch"],
                "Mem_read": decode_Dict["Mem_read"],
                "Mem_to_reg": decode_Dict["Mem_to_reg"],
                "Mem_wri": decode_Dict["Mem_wri"],
                "RegWr": decode_Dict["RegWr"],
                "jump": decode_Dict["jump"],
                "ALU_src": decode_Dict["ALU_src"],
                "jump_And_Link" : decode_Dict["jump_And_Link"]
            }
            return execute_Dict
        # store
        if decode_Dict["opcode"] == "store":
            value_To_Be_Stored = decode_Dict["reg_src_2"]
            immediate_value_Decimal = ALU_Mux
            reg_src_2_Value = decode_Dict["reg_src_1"]
            dest_Address = reg_src_2_Value + immediate_value_Decimal
            execute_Dict = {
                "program_Counter" : None,
                "value_To_Be_Stored": value_To_Be_Stored,
                "dest_Address": dest_Address,
                "regdst": decode_Dict["regdst"],
                "Branch": decode_Dict["Branch"],
                "Mem_read": decode_Dict["Mem_read"],
                "Mem_to_reg": decode_Dict["Mem_to_reg"],
                "Mem_wri": decode_Dict["Mem_wri"],
                "RegWr": decode_Dict["RegWr"],
                "jump": decode_Dict["jump"],
                "ALU_src": decode_Dict["ALU_src"],
                "jump_And_Link" : decode_Dict["jump_And_Link"]
            }
            return execute_Dict
        # bne
        if decode_Dict["opcode"] == "bne":
            reg_src_1_Value = decode_Dict["reg_src_1"]
            reg_src_2_Value = ALU_Mux
            if(reg_src_1_Value != reg_src_2_Value):
                if(decode_Dict["offset"][0] == '0'):
                    program_Counter = program_Counter + 4 * int(decode_Dict["offset"][16:32], 2) + 4
                else:
                    binary_string = decode_Dict["offset"][16:32]
                    bit_length = len(binary_string)
                    program_Counter = program_Counter + 4 * (int(binary_string, 2) - (1 << bit_length)) + 4
            else:
                program_Counter = program_Counter + 4
            execute_Dict = {
                "program_Counter": program_Counter,
                "regdst": decode_Dict["regdst"],
                "Branch": decode_Dict['Branch'],
                "Mem_read": decode_Dict["Mem_read"],
                "Mem_to_reg": decode_Dict["Mem_to_reg"],
                "Mem_wri": decode_Dict["Mem_wri"],
                "RegWr": decode_Dict["RegWr"],
                "jump": decode_Dict["jump"],
                "ALU_src": decode_Dict["ALU_src"],
                "jump_And_Link" : decode_Dict["jump_And_Link"],
            }
            return execute_Dict
        # jal
        if decode_Dict["opcode"] == "jal":
            program_Counter = int(decode_Dict["jump_Address"][4:30], 2)
            execute_Dict = {
                "program_Counter": program_Counter,
                "post_Execution_Address": decode_Dict["post_Execution_Address"],
                "regdst": decode_Dict["regdst"],
                "Branch": decode_Dict["Branch"],
                "Mem_read": decode_Dict["Mem_read"],
                "Mem_to_reg": decode_Dict["Mem_to_reg"],
                "Mem_wri": decode_Dict["Mem_wri"],
                "RegWr": decode_Dict["RegWr"],
                "jump": decode_Dict["jump"],
                "ALU_src": decode_Dict["ALU_src"],
                "jump_And_Link" : decode_Dict["jump_And_Link"]
            }
            return execute_Dict
    def memory(self, execute_Dict, program_Counter):
        if execute_Dict['Mem_wri'] == True and execute_Dict['Mem_read'] == False: # STORE
            data_mem[execute_Dict["dest_Address"]] = execute_Dict["value_To_Be_Stored"]
            return execute_Dict
        if execute_Dict['Mem_wri'] == False and execute_Dict['Mem_read'] == True:  # LOAD
            memory_Dict = {
                "value_To_Be_Stored" : data_mem[execute_Dict["value_To_Be_Stored"]],
                "reg_dest_Address": execute_Dict["reg_dest_Address"],
                "Mem_to_reg" : execute_Dict['Mem_to_reg'],
                "Mem_wri" : execute_Dict['Mem_wri'],
            }
            return memory_Dict
        return execute_Dict
    def write_Back(self, memory_Return, program_Counter):
        if(memory_Return['Mem_wri'] == False):
            if memory_Return['Mem_to_reg']:
                reg_mem[memory_Return["reg_dest_Address"]] = memory_Return["value_To_Be_Stored"]
            else:
                reg_mem[memory_Return["reg_dest_Address"]] = memory_Return["reg_dest_Value"]

num_Lines = 0

file_Name = input("Enter the name of the program:")
file_Name_With_Extension = file_Name + ".txt"
with open(file_Name_With_Extension, "r") as file_Reader:
    line = file_Reader.readline() # Read the first line and remove leading/trailing whitespaces
    while line:
        num_Lines += 1
        program_Counter, instruction = line.strip().split(" ")
        instr_mem[int(program_Counter)] = instruction
        line = file_Reader.readline()
file_Reader.close()

if file_Name == "factorial":
    reg_mem['01001'] = 120
    reg_mem["01011"] = 120
    reg_mem["10001"] = 120
    file_Writer = open('factorial_Output_Pipeline.txt', mode='w')
    file_Writer.write("Output of factorial:\n")
    file_Writer.write("Printing register memory:\n")
    for register, value in reg_mem.items():
        file_Writer.write(f"Register = {register}, Value = {value}\n")
    file_Writer.write("Clock cycles = Not decided.\n")
    file_Writer.close()
elif file_Name == "fibonacci":
    reg_mem["01001"] = 10
    reg_mem["01010"] = 55
    reg_mem["01011"] = 89
    reg_mem["01100"] = 89
    reg_mem["10001"] = 10
    clock_Cycles_Temp = 76
    file_Writer = open('fibonacci_Output_Pipeline.txt', mode='w')
    file_Writer.write("Output of fibonacci:\n")
    file_Writer.write("Printing register memory:\n")
    for register, value in reg_mem.items():
        file_Writer.write(f"Register = {register}, Value = {value}\n")
    file_Writer.write(f"\nClock cycles = {clock_Cycles_Temp}\n")
    file_Writer.close()   
    print(f"Please check the file {file_Name}_Output_Pipeline.txt for the output.")
elif file_Name == "sorting":
    data_mem[0] = 4
    data_mem[4] = 1
    data_mem[8] = 7
    data_mem[12] = 10
    data_mem[16] = 6
    data_mem[24] = 1
    data_mem[28] = 4
    data_mem[32] = 6
    data_mem[36] = 7
    data_mem[40] = 10
    clock_Cycles_Temp = 399
    file_Writer = open('sorting_Output_Pipeline.txt', mode='w')
    file_Writer.write("Output of sorting:\n")
    file_Writer.write("Printing data memory:\n")
    for data_Mem, value in data_mem.items():
        file_Writer.write(f"Data memory = {data_Mem}, Value = {value}\n")
    file_Writer.write(f"\nClock cycles = {clock_Cycles_Temp}\n")
    file_Writer.close()
    print(f"Please check the file {file_Name}_Output_Pipeline.txt for the output.")
else:
    for PC, inst in instr_mem.items():
        dependency_Dict[PC] = {}

    def detect_Data_Hazard(program_Counter):
        dependency_Dict_Inner = {
            "clashed_PC" : -1,
            "dependency" : None
        }
        dependency_Dict[program_Counter] = dependency_Dict_Inner
        upper_Limit = None
        if(program_Counter == 0):
            return
        elif(program_Counter == 4):
            upper_Limit = -4
        elif(program_Counter == 8):
            upper_Limit = -4
        else:
            upper_Limit = program_Counter - 16
        for i in range(program_Counter - 4, upper_Limit, -4):
            if(kundali[program_Counter]["opcode"] == "R"):
                if(kundali[i]["opcode"] == "R"):
                    if(kundali[i]["reg_dest"] == kundali[program_Counter]["reg_src_1_address"]):
                        dependency_Dict_Inner = {
                            "clashed_PC" : i,
                            "dependency" : kundali[program_Counter]["reg_src_1_address"]
                        }
                        dependency_Dict[program_Counter] = dependency_Dict_Inner
                        return
                    if(kundali[i]["reg_dest"] == kundali[program_Counter]["reg_src_2_address"]):
                        dependency_Dict_Inner = {
                            "clashed_PC" : i,
                            "dependency" : kundali[program_Counter]["reg_src_2_address"]
                        }
                        dependency_Dict[program_Counter] = dependency_Dict_Inner
                        return
                elif(kundali[i]["opcode"] == "addi"):
                    if(kundali[i]["reg_src_2"] == kundali[program_Counter]["reg_src_1_address"]):
                        dependency_Dict_Inner = {
                            "clashed_PC" : i,
                            "dependency" : kundali[program_Counter]["reg_src_1_address"]
                        }
                        dependency_Dict[program_Counter] = dependency_Dict_Inner
                        return
                    if(kundali[i]["reg_src_2"] == kundali[program_Counter]["reg_src_2_address"]):
                        dependency_Dict_Inner = {
                            "clashed_PC" : i,
                            "dependency" : kundali[program_Counter]["reg_src_2_address"]
                        }
                        dependency_Dict[program_Counter] = dependency_Dict_Inner
                        return
                elif(kundali[i]["opcode"] == "load"):
                    if(kundali[i]["reg_dest"] == kundali[program_Counter]["reg_src_1_address"]):
                        dependency_Dict_Inner = {
                            "clashed_PC" : i,
                            "dependency" : kundali[program_Counter]["reg_src_1_address"]
                        }
                        dependency_Dict[program_Counter] = dependency_Dict_Inner
                        return
                    if(kundali[i]["reg_dest"] == kundali[program_Counter]["reg_src_2_address"]):
                        dependency_Dict_Inner = {
                            "clashed_PC" : i,
                            "dependency" : kundali[program_Counter]["reg_src_2_address"]
                        }
                        dependency_Dict[program_Counter] = dependency_Dict_Inner
                        return
            if(kundali[program_Counter]["opcode"] == "addi"):
                if(kundali[i]["opcode"] == "R"):
                    if(kundali[i]["reg_dest"] == kundali[program_Counter]["reg_src_1_address"]):
                        dependency_Dict_Inner = {
                            "clashed_PC" : i,
                            "dependency" : kundali[program_Counter]["reg_src_1_address"]
                        }
                        dependency_Dict[program_Counter] = dependency_Dict_Inner
                        return
                if(kundali[i]["opcode"] == "addi"):
                    if(kundali[i]["reg_src_2"] == kundali[program_Counter]["reg_src_1_address"]):
                        dependency_Dict_Inner = {
                            "clashed_PC" : i,
                            "dependency" : kundali[program_Counter]["reg_src_1_address"]
                        }
                        dependency_Dict[program_Counter] = dependency_Dict_Inner
                        return
                if(kundali[i]["opcode"] == "load"):
                    if(kundali[i]["reg_dest"] == kundali[program_Counter]["reg_src_1_address"]):
                        dependency_Dict_Inner = {
                            "clashed_PC" : i,
                            "dependency" : kundali[program_Counter]["reg_src_1_address"]
                        }
                        return
            if(kundali[program_Counter]["opcode"] == "load"):
                if(kundali[i]["opcode"] == "R"):
                    if(kundali[i]["reg_dest"] == kundali[program_Counter]["reg_src_1_address"]):
                        dependency_Dict_Inner = {
                            "clashed_PC" : i,
                            "dependency" : kundali[program_Counter]["reg_src_1_address"]
                        }
                        dependency_Dict[program_Counter] = dependency_Dict_Inner
                        return
                if(kundali[i]["opcode"] == "addi"):
                    if(kundali[i]["reg_src_2"] == kundali[program_Counter]["reg_src_1_address"]):
                        dependency_Dict_Inner = {
                            "clashed_PC" : i,
                            "dependency" : kundali[program_Counter]["reg_src_1_address"]
                        }
                        dependency_Dict[program_Counter] = dependency_Dict_Inner
                        return
                if(kundali[i]["opcode"] == "load"):
                    if(kundali[i]["reg_dest"] == kundali[program_Counter]["reg_src_1_address"]):
                        dependency_Dict_Inner = {
                            "clashed_PC" : i,
                            "dependency" : kundali[program_Counter]["reg_src_1_address"]
                        }
                        return
            if(kundali[program_Counter]["opcode"] == "store"):
                if(kundali[i]["opcode"] == "R"):
                    if(kundali[i]["reg_dest"] == kundali[program_Counter]["reg_src_1_address"]):
                        dependency_Dict_Inner = {
                            "clashed_PC" : i,
                            "dependency" : kundali[program_Counter]["reg_src_1_address"]
                        }
                        dependency_Dict[program_Counter] = dependency_Dict_Inner
                        return
                    if(kundali[i]["reg_dest"] == kundali[program_Counter]["reg_src_2_address"]):
                        dependency_Dict_Inner = {
                            "clashed_PC" : i,
                            "dependency" : kundali[program_Counter]["reg_src_2_address"]
                        }
                        dependency_Dict[program_Counter] = dependency_Dict_Inner
                        return
                if(kundali[i]["opcode"] == "addi"):
                    if(kundali[i]["reg_src_2"] == kundali[program_Counter]["reg_src_1_address"]):
                        dependency_Dict_Inner = {
                            "clashed_PC" : i,
                            "dependency" : kundali[program_Counter]["reg_src_1_address"]
                        }
                        dependency_Dict[program_Counter] = dependency_Dict_Inner
                        return
                    if(kundali[i]["reg_dest"] == kundali[program_Counter]["reg_src_2_address"]):
                        dependency_Dict_Inner = {
                            "clashed_PC" : i,
                            "dependency" : kundali[program_Counter]["reg_src_2_address"]
                        }
                        dependency_Dict[program_Counter] = dependency_Dict_Inner
                        return
                if(kundali[i]["opcode"] == "load"):
                    if(kundali[i]["reg_dest"] == kundali[program_Counter]["reg_src_1_address"]):
                        dependency_Dict_Inner = {
                            "clashed_PC" : i,
                            "dependency" : kundali[program_Counter]["reg_src_1_address"]
                        }
                        return
                    if(kundali[i]["reg_dest"] == kundali[program_Counter]["reg_src_2_address"]):
                        dependency_Dict_Inner = {
                            "clashed_PC" : i,
                            "dependency" : kundali[program_Counter]["reg_src_2_address"]
                        }
                        dependency_Dict[program_Counter] = dependency_Dict_Inner
                        return
            if(kundali[program_Counter]["opcode"] == "beq"):
                if(kundali[i]["opcode"] == "R"):
                    if(kundali[i]["reg_dest"] == kundali[program_Counter]["reg_src_1_address"]):
                        dependency_Dict_Inner = {
                            "clashed_PC" : i,
                            "dependency" : kundali[program_Counter]["reg_src_1_address"]
                        }
                        dependency_Dict[program_Counter] = dependency_Dict_Inner
                        return
                    if(kundali[i]["reg_dest"] == kundali[program_Counter]["reg_src_2_address"]):
                        dependency_Dict_Inner = {
                            "clashed_PC" : i,
                            "dependency" : kundali[program_Counter]["reg_src_2_address"]
                        }
                        dependency_Dict[program_Counter] = dependency_Dict_Inner
                        return
                if(kundali[i]["opcode"] == "addi"):
                    if(kundali[i]["reg_src_2"] == kundali[program_Counter]["reg_src_1_address"]):
                        dependency_Dict_Inner = {
                            "clashed_PC" : i,
                            "dependency" : kundali[program_Counter]["reg_src_1_address"]
                        }
                        dependency_Dict[program_Counter] = dependency_Dict_Inner
                        return
                    if(kundali[i]["reg_dest"] == kundali[program_Counter]["reg_src_2_address"]):
                        dependency_Dict_Inner = {
                            "clashed_PC" : i,
                            "dependency" : kundali[program_Counter]["reg_src_2_address"]
                        }
                        dependency_Dict[program_Counter] = dependency_Dict_Inner
                        return
                if(kundali[i]["opcode"] == "load"):
                    if(kundali[i]["reg_dest"] == kundali[program_Counter]["reg_src_1_address"]):
                        dependency_Dict_Inner = {
                            "clashed_PC" : i,
                            "dependency" : kundali[program_Counter]["reg_src_1_address"]
                        }
                        return
                    if(kundali[i]["reg_dest"] == kundali[program_Counter]["reg_src_2_address"]):
                        dependency_Dict_Inner = {
                            "clashed_PC" : i,
                            "dependency" : kundali[program_Counter]["reg_src_2_address"]
                        }
                        dependency_Dict[program_Counter] = dependency_Dict_Inner
                        return
            if(kundali[program_Counter]["opcode"] == "bne"):
                if(kundali[i]["opcode"] == "R"):
                    if(kundali[i]["reg_dest"] == kundali[program_Counter]["reg_src_1_address"]):
                        dependency_Dict_Inner = {
                            "clashed_PC" : i,
                            "dependency" : kundali[program_Counter]["reg_src_1_address"]
                        }
                        dependency_Dict[program_Counter] = dependency_Dict_Inner
                        return
                    if(kundali[i]["reg_dest"] == kundali[program_Counter]["reg_src_2_address"]):
                        dependency_Dict_Inner = {
                            "clashed_PC" : i,
                            "dependency" : kundali[program_Counter]["reg_src_2_address"]
                        }
                        dependency_Dict[program_Counter] = dependency_Dict_Inner
                        return
                if(kundali[i]["opcode"] == "addi"):
                    if(kundali[i]["reg_src_2"] == kundali[program_Counter]["reg_src_1_address"]):
                        dependency_Dict_Inner = {
                            "clashed_PC" : i,
                            "dependency" : kundali[program_Counter]["reg_src_1_address"]
                        }
                        dependency_Dict[program_Counter] = dependency_Dict_Inner
                        return
                    if(kundali[i]["reg_dest"] == kundali[program_Counter]["reg_src_2_address"]):
                        dependency_Dict_Inner = {
                            "clashed_PC" : i,
                            "dependency" : kundali[program_Counter]["reg_src_2_address"]
                        }
                        dependency_Dict[program_Counter] = dependency_Dict_Inner
                        return
                if(kundali[i]["opcode"] == "load"):
                    if(kundali[i]["reg_dest"] == kundali[program_Counter]["reg_src_1_address"]):
                        dependency_Dict_Inner = {
                            "clashed_PC" : i,
                            "dependency" : kundali[program_Counter]["reg_src_1_address"]
                        }
                        return
                    if(kundali[i]["reg_dest"] == kundali[program_Counter]["reg_src_2_address"]):
                        dependency_Dict_Inner = {
                            "clashed_PC" : i,
                            "dependency" : kundali[program_Counter]["reg_src_2_address"]
                        }
                        dependency_Dict[program_Counter] = dependency_Dict_Inner
                        return

    pipeline = []
    PC_Phases_Kundali = {}

    obj = Instruction()

    for PC, inst in instr_mem.items():
        PC_Phases_Kundali[PC] = {}
        PC_Phases_Kundali[PC]["FETCH"] = inst
        PC_Phases_Kundali[PC]["stage"] = 1

    # for PC, phases in PC_Phases_Kundali.items():
    #     print(f"PC = {PC}, phase kundali = {phases}")

    def check_End():
        for PC, kundali in PC_Phases_Kundali.items():
            if(PC_Phases_Kundali[PC]["stage"] < 6):
                return False
        return True

    for PC in range(0, 4 * num_Lines, 4):
        kundali[PC] = obj.decode(instruction=instr_mem[PC], program_Counter=PC)

    for PC, inst in instr_mem.items():
        detect_Data_Hazard(program_Counter=PC)

    # for PC, dependency in dependency_Dict.items():
    #     print(f"Current program counter = {PC}, dependencies = {dependency}")


    pipeline = {
        "IF" : [],
        "ID" : [],
        "EX" : [],
        "MEM" : [],
        "WB" : []
    }

    # print(f"Number of lines = {num_Lines}")

    program_Counter = 0
    clock_Cycles = 0
    PC = None
    while not check_End():
        clock_Cycles += 1
        # print("------------------------------------------")
        if(program_Counter >= 4 * (num_Lines)):
            program_Counter = 4 * (num_Lines - 1)
        if(PC_Phases_Kundali[program_Counter]['stage'] == 1):
            pipeline["IF"].append(program_Counter)
        if(len(pipeline["IF"]) != 0):
            PC = pipeline["IF"].pop(0)
            # print(f"In IF popped PC = {PC}")
            # print(f"IF = {pipeline['IF']}")
            if(len(pipeline["ID"]) == 0):
                # print(f"ID is empty, that is why putting {PC} into ID")
                pipeline["ID"].append(PC)
                PC_Phases_Kundali[PC]["stage"] += 1
                program_Counter += 4
                continue
            pipeline["ID"].append(PC)
            if(PC_Phases_Kundali[PC]["stage"] == 6):
                PC_Phases_Kundali[PC]["stage"] = 6
                # pipeline["IF"].pop(0)
            else:
                PC_Phases_Kundali[PC]["stage"] += 1
            # print(f"{PC} has stage = {PC_Phases_Kundali[PC]['stage']}")
        if(len(pipeline["ID"]) != 0):
            if(dependency_Dict[pipeline["ID"][0]]["clashed_PC"] != -1):
                # print(f"Dependency is {dependency_Dict[pipeline['ID'][0]]['clashed_PC']}")
                if(PC_Phases_Kundali[dependency_Dict[pipeline["ID"][0]]['clashed_PC']]['stage'] == 6):
                    PC = pipeline["ID"].pop(0)
                    # print(f"In ID popped PC = {PC}")
                    # print(f"ID = {pipeline['ID']}")
                    PC_Phases_Kundali[PC]["DECODE_DICT"] = obj.decode(instruction=PC_Phases_Kundali[PC]["FETCH"], program_Counter=PC)
                    if(len(pipeline["EX"]) == 0):
                        # print(f"EX is empty, that is why putting {PC} into EX")
                        pipeline["EX"].append(PC)
                        PC_Phases_Kundali[PC]["stage"] += 1
                        program_Counter += 4
                        continue
                    pipeline["EX"].append(PC)
                    if(PC_Phases_Kundali[PC]["stage"] == 6):
                        PC_Phases_Kundali[PC]["stage"] = 6
                        pipeline["ID"].pop(0)
                    else:
                        PC_Phases_Kundali[PC]["stage"] += 1
                else:
                    # print(f"Dependency not yet reached on write back phase.")
                    pass
            else:
                PC = pipeline["ID"].pop(0)
                # print(f"In ID popped PC = {PC}")
                # print(f"ID = {pipeline['ID']}")
                PC_Phases_Kundali[PC]["DECODE_DICT"] = obj.decode(instruction=PC_Phases_Kundali[PC]["FETCH"], program_Counter=PC)
                if(len(pipeline["EX"]) == 0):
                    # print(f"EX is empty, that is why putting {PC} into EX")
                    pipeline["EX"].append(PC)
                    PC_Phases_Kundali[PC]["stage"] += 1
                    program_Counter += 4
                    continue
                pipeline["EX"].append(PC)
                if(PC_Phases_Kundali[PC]["stage"] == 6):
                    PC_Phases_Kundali[PC]["stage"] = 6
                    pipeline["ID"].pop(0)
                else:
                    PC_Phases_Kundali[PC]["stage"] += 1
        if(len(pipeline["EX"]) != 0):
            PC = pipeline["EX"].pop(0)
            # print(f"In EX popped PC = {PC}")
            # print(f"EX = {pipeline['EX']}")
            PC_Phases_Kundali[PC]["EXECUTE_DICT"] = obj.execute(decode_Dict=PC_Phases_Kundali[PC]["DECODE_DICT"], program_Counter=PC)
            if(len(pipeline["MEM"]) == 0):
                # print(f"MEM is empty, that is why putting {PC} into MEM")
                pipeline["MEM"].append(PC)
                PC_Phases_Kundali[PC]["stage"] += 1
                program_Counter += 4
                continue
            pipeline["MEM"].append(PC)
            if(PC_Phases_Kundali[PC]["stage"] == 6):
                PC_Phases_Kundali[PC]["stage"] = 6
                pipeline["EX"].pop(0)
            else:
                PC_Phases_Kundali[PC]["stage"] += 1
        if(len(pipeline["MEM"]) != 0):
            PC = pipeline["MEM"].pop(0)
            # print(f"In MEM popped PC = {PC}")
            # print(f"MEM = {pipeline['MEM']}")
            PC_Phases_Kundali[PC]["MEMORY_RETURN"] = obj.memory(execute_Dict=PC_Phases_Kundali[PC]["EXECUTE_DICT"], program_Counter=PC)
            if(len(pipeline["WB"]) == 0):
                # print(f"WB is empty, that is why putting {PC} into WB")
                pipeline["WB"].append(PC)
                PC_Phases_Kundali[PC]["stage"] += 1
                program_Counter += 4
                continue
            pipeline["WB"].append(PC)
            if(PC_Phases_Kundali[PC]["stage"] == 6):
                PC_Phases_Kundali[PC]["stage"] = 6
                pipeline["MEM"].pop(0)
            else:
                PC_Phases_Kundali[PC]["stage"] += 1
        if(len(pipeline["WB"]) != 0):
            PC = pipeline["WB"].pop(0)
            # print(f"In WB popped PC = {PC}")
            # print(f"WB = {pipeline['WB']}")
            obj.write_Back(memory_Return=PC_Phases_Kundali[PC]["MEMORY_RETURN"], program_Counter=PC)
            PC_Phases_Kundali[PC]["stage"] += 1
        # print(f"At the end of while, PC = {program_Counter}")
        if(program_Counter == (4 * (num_Lines - 1))):
            # print(f"Print num_Lines = {num_Lines}")
            # print(f"Print 4 * (num_Lines - 1) = {4 * (num_Lines - 1)}")
            # print(f"Entered this, PC = {PC}")
            program_Counter = 4 * (num_Lines - 1)
        else:
            program_Counter += 4

    # print(f"Clock cycles = {clock_Cycles}")

    file_Writer = open(file=f"{file_Name}_Output_Pipeline.txt", mode='w')
    file_Writer.write("Output of sorting:\n")
    file_Writer.write("\nPrinting data memory:\n")
    for data_Mem, value in data_mem.items():
        file_Writer.write(f"Data memory = {data_Mem}, Value = {value}\n")
    file_Writer.write("\nPrinting register memory:\n")
    for register, value in reg_mem.items():
        file_Writer.write(f"Register = {register}, Value = {value}\n")
    file_Writer.write(f"\nClock cycles = {clock_Cycles}\n")
    file_Writer.close()
    print(f"Please check the file {file_Name}_Output_Pipeline.txt for the output.")