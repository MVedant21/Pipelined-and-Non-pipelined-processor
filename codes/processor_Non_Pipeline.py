# reg_dest_mem = {}
# reg_source_mem = {}
import time
instr_mem = {}
data_mem = {}
for i in range(101):
    data_mem[i] = 0
data_mem[0] = 4
data_mem[4] = 1
data_mem[8] = 7
data_mem[12] = 10
data_mem[16] = 6
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
    "01001": 5,
    "01010": 0,
    "01011": 24,
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
    "1001010": "or",
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

program_Counter = 1

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


# --------------DECODE PHASE------------------


def decode(instruction, program_Counter):
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
            "reg_src_2": reg_Dest, # 10001
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
            "reg_src_2": reg_mem[instruction[11:16]],
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
            "reg_src_2": reg_mem[instruction[11:16]],
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
            "reg_src_2": reg_mem[instruction[11:16]],
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
    
# --------------EXECUTE PHASE------------------

def execute(decode_Dict, program_Counter):
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


# --------------MEMORY PHASE------------------


def memory(execute_Dict, program_Counter):
    if execute_Dict['Mem_wri'] == True and execute_Dict['Mem_read'] == False: # STORE
        data_mem[execute_Dict["dest_Address"]] = execute_Dict["value_To_Be_Stored"]
        return execute_Dict
    if execute_Dict['Mem_wri'] == False and execute_Dict['Mem_read'] == True:  # LOAD
        memory_Dict = {
            "value_To_Be_Stored" : data_mem[execute_Dict["value_To_Be_Stored"]],
            "reg_dest_Address": execute_Dict["reg_dest_Address"],
            "Mem_to_reg" : execute_Dict['Mem_to_reg'],
            "Mem_wri" : execute_Dict['Mem_wri']
        }
        return memory_Dict
    return execute_Dict

# -----------------------WRITE BACK PHASE------------------------


def write_Back(memory_Return, program_Counter):
    if(memory_Return['Mem_wri'] == False):
        if memory_Return['Mem_to_reg']:
            reg_mem[memory_Return["reg_dest_Address"]] = memory_Return["value_To_Be_Stored"]
        else:
            reg_mem[memory_Return["reg_dest_Address"]] = memory_Return["reg_dest_Value"]

num_Lines = 0
clock_Cycles = 0
file_Name = input("Write the program name:")
file_Name_With_Extension = file_Name + ".txt"
with open(file_Name_With_Extension, "r") as read_Binary:
    line = read_Binary.readline() # Read the first line and remove leading/trailing whitespaces
    while line:
        num_Lines += 1
        program_Counter, instruction = line.strip().split(" ")
        instr_mem[int(program_Counter)] = instruction
        line = read_Binary.readline()
read_Binary.close()

program_Counter = 0
while program_Counter < (num_Lines * 4):
    clock_Cycles += 5
    instruction = instr_mem[int(program_Counter)]
    decode_Dict = decode(instruction=instruction, program_Counter=program_Counter)
    execute_Dict = execute(decode_Dict=decode_Dict, program_Counter=program_Counter)
    if execute_Dict['jump']: # JUMP/BEQ/BNE
        program_Counter = execute_Dict['program_Counter']
    elif execute_Dict['Branch']:
        program_Counter = execute_Dict['program_Counter']
    else:
        memory_Return = memory(execute_Dict=execute_Dict, program_Counter=program_Counter)
        if(execute_Dict['Mem_wri'] == False):
            write_Back(memory_Return=memory_Return, program_Counter=program_Counter)
        program_Counter += 4

file_Writer = open(file=file_Name + "_Non_Pipeline_Output.txt", mode="w")
file_Writer.write(f"Output for {file_Name} program:\n")
if(file_Name == "factorial" or file_Name == "fibonacci"):
    file_Writer.write("Printing register memory:\n\n")
    for register, value in reg_mem.items():
        file_Writer.write(f"Register = {register}, Value = {value}\n")
else:
    file_Writer.write("Printing data memory:\n")
    for address, value in data_mem.items():
        file_Writer.write(f"Address = {address}, value = {value}\n")  
file_Writer.write(f"\nClock cycles required = {clock_Cycles}")
output_File_Name = file_Name + "_Non_Pipeline_Output.txt"
print(f"Please check {output_File_Name} for the output")
file_Writer.close()