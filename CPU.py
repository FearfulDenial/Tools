from dataclasses import dataclass
from enum import Enum

#* Variables
Variables = [
    ResetVector = 0xFFFC, #? Reset Vector
    IrqVector = 0xFFFE, #? Interrupt Request Vector
    NmiVector = 0xFFFA, #? Non-Maskable Interrupt Vector
]

RESET_VECTOR = 0xFFFC
IRQ_VECTOR = 0xFFFE
NMI_VECTOR = 0xFFFA
#* Register
@dataclass
class Registers:
    A: int = 0 #? Accumulator
    X: int = 0 #? Index Register X
    Y: int = 0 #? Index Register Y
    Pc: int = 0 #? Program Counter
    Sp: int = 0xFF #? Stack Pointer
    Sr: int = 0 #? Status Register
#* Memory
MemorySize = 65536 # 64KB
Memory = [0] * MemorySize
#* Instructions
class OPCODE(Enum):
    LDA_IMM = 0xA9 #? Load Accumulator with Immediate Value
    LDA_ZP = 0xA5 #? Load Accumulator with Zero-Page Address
    STA_ABS = 0x8D #? Store Accumulator with Absolute Address
    JMP_ABS = 0x4C #? Jump to Absolute Address
    ADC_IMM = 0x69 #? Add Accumulator with Immediate Value and Carry
    PHA = 0x48 #? Push Accumulator onto Stack
    BEQ = 0xF0 #? Branch if Equal

def Flags(Opcode,**Kwargs):
    if Opcode == "UPDATE":
        Registers = Kwargs.get("registers")
        Value = Kwargs.get("value")
        if not Registers or not Value: return False,f"Required Parameters not found for OPCODE '{Opcode}' to be ran."
        Registers.Sr = 0
        if Value == 0: Registers.Sr |= 0x02 #? Zero
        if Value & 0x80: Registers.Sr |= 0x80 #? Negative
    else:
        return False,NotImplementedError,f"FLAGS Opcode '{Opcode}' is not implemented."
    return True,"Operation completed."
def Vector(Opcode,**Kwargs):
    if Opcode == "RESET":
        Registers = Kwargs.get("registers")
        Memory = Kwargs.get("memory")
        if not Registers or not Memory: return False,f"Required Parameters not found for OPCODE '{Opcode}' to be ran."
        Registers.Pc = Memory[Variables.]
def reset(Registers, Memory):
    Registers.Pc = Memory[RESET_VECTOR] | (Memory[RESET_VECTOR + 1] << 8)
    Registers.Sp = 0xFF
    Registers.Sr = 0x00
def ALU(Opcode,Operand1,Operand2):
    if Opcode == "ADD":
        Result = Operand1 + Operand2
        Flags("UPDATE",Registers=Registers,Value=Result & 0xFF)
        return True,Result & 0xFF
    elif Opcode == "AND":
        return True,Operand1 & Operand2
    else:
        return False,NotImplementedError,f"ALU Opcode '{Opcode}' is not implemented."

def Execute(Registers, Memory):
    Opcode = Memory[Registers.Pc]
    if Opcode == OPCODE.BEQ.value:
        Registers.Pc += 1
        Offset = Memory[Registers.Pc]
        if Registers.Sr & 0x02:
            Registers.Pc += Offset if Offset < 0x80 else Offset - 0x100
        else:
            Registers.Pc += 1
    elif Opcode == OPCODE.PHA.value:
        Memory[Registers.Sp] = Registers.A
        Registers.Sp -= 1
        Registers.Pc += 1
    elif Opcode == OPCODE.LDA_ZP.value:
        Registers.Pc += 1
        Address = Memory[Registers.Pc]
        Registers.A = Memory[Address]
        Registers.Pc += 1
    elif Opcode == OPCODE.ADC_IMM.value:
        Registers.Pc += 1
        Value = Memory[Registers.Pc]
        Registers.A = ALU("ADD", Registers.A, Value)
        Registers.Pc += 1
    elif Opcode == OPCODE.LDA_IMM.value:
        Registers.Pc += 1
        Registers.A = Memory[Registers.Pc]
        Registers.Pc += 1
    elif Opcode == OPCODE.STA_ABS.value:
        Address = Memory[Registers.Pc + 1] | (Memory[Registers.Pc + 2] << 8)
        Memory[Address] = Registers.A
        Registers.Pc += 3
    elif Opcode == OPCODE.JMP_ABS.value:
        Address = Memory[Registers.Pc + 1] | (Memory[Registers.Pc + 2] << 8)
        Registers.Pc = Address
    else:
        return False,NotImplementedError,f"EXE Opcode '{Opcode}' is not implemented."
    return True,"Operation completed."