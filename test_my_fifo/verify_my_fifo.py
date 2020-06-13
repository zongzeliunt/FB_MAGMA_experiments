import my_fifo
import magma as m
import fault

from typing import List, Union, Tuple
from hwtypes import Enum, Product, Bit, BitVector

import pprint
pp = pprint.PrettyPrinter()

datatype = m.UInt[32]
data_width = 32
def default_INTERFACE_instance(INTERFACE):
#{{{
    """
    Convenience function to instantiate an _APB object with default values of 0
    """
    fields = {}
    for key, value in INTERFACE.field_dict.items():
        fields[key] = value(0)
    return INTERFACE(**fields)
#}}}

def FIFO_interface_value_dict (data_width):
#{{{
	fields = {}
	fields.update({	
		"CLK"  : Bit,
        "RESET": Bit,
		"WData": BitVector[data_width],
		"Full":  Bit,
		"Write": Bit,
		"RData": BitVector[data_width],
		"Empty": Bit,
		"Read":  Bit
	})
	result = type("FIFO_interface_value_dict", (Product, ), fields)
	return result
#}}}


#RUN
#=========================================================

#1) 在这里声明waveform 
#=========================================================
"""
interface_value_dict = FIFO_interface_value_dict(data_width)

print (interface_value_dict)
print (interface_value_dict.field_dict)
print (interface_value_dict.field_dict.items())
for key, value in interface_value_dict.field_dict.items():
	print (str(key) + " : ", str(value))

interface_obj = default_INTERFACE_instance(interface_value_dict)
print (interface_obj)
"""











#2) 声明FIFO 
#=========================================================
interface = my_fifo.make_HandshakeData(datatype)



FIFO = my_fifo.FIFOGenerator(interface, 4)

fields = (field for field in FIFO.ARES_design)


tester = fault.Tester(FIFO, clock=FIFO.ARES_design.CLK)

#从这里开始，每两个step代表一个cycle
#一定得是两个step代表一个cycle！切记！
#cycle 0
tester.circuit.ARES_design.RESET = 1
tester.step(2)

#cycle 1
tester.circuit.ARES_design.RESET = 0 
tester.step(2)

#cycle 2 
#写15
tester.circuit.ARES_design.Empty.expect(1)
tester.circuit.ARES_design.Full.expect(0)
tester.circuit.ARES_design.Write = True 
tester.circuit.ARES_design.WData = 15
tester.step(2)

#cycle 3
#写16
tester.circuit.ARES_design.Empty.expect(0)
tester.circuit.ARES_design.Full.expect(0)
tester.circuit.ARES_design.Write = True
tester.circuit.ARES_design.WData = 16
tester.step(2)

#cycle 4
#写17
tester.circuit.ARES_design.Empty.expect(0)
tester.circuit.ARES_design.Full.expect(0)
tester.circuit.ARES_design.Write = True
tester.circuit.ARES_design.WData = 17
tester.step(2)

#cycle 5
#写18
tester.circuit.ARES_design.Empty.expect(0)
tester.circuit.ARES_design.Full.expect(0)
tester.circuit.ARES_design.Write = True
tester.circuit.ARES_design.WData = 18
tester.step(2)

#cycle 6 
#full 为1
#读15
tester.circuit.ARES_design.Empty.expect(0)
tester.circuit.ARES_design.Full.expect(1)
tester.circuit.ARES_design.Write = False 
tester.circuit.ARES_design.RData.expect(15)
tester.circuit.ARES_design.Read = True
tester.step(2)

#cycle 7
#full 为0
#这个地方才是精妙的地方，读一个数full立刻变0
#读16
tester.circuit.ARES_design.Empty.expect(0)
tester.circuit.ARES_design.Full.expect(0)
tester.circuit.ARES_design.RData.expect(16)
tester.circuit.ARES_design.Read = True
tester.step(2)

#cycle 8 
#读17
tester.circuit.ARES_design.Empty.expect(0)
tester.circuit.ARES_design.Full.expect(0)
tester.circuit.ARES_design.RData.expect(17)
tester.circuit.ARES_design.Read = True
tester.step(2)

#cycle 9 
#读18
tester.circuit.ARES_design.Empty.expect(0)
tester.circuit.ARES_design.Full.expect(0)
tester.circuit.ARES_design.RData.expect(18)
tester.circuit.ARES_design.Read = True
tester.step(2)

#cycle 10 
#读18
tester.circuit.ARES_design.Empty.expect(1)
tester.circuit.ARES_design.Full.expect(0)
tester.circuit.ARES_design.Read = False
tester.step(2)

print (tester)
"""
Actions:
    0: Poke(FIFOGenerator.ARES_design.CLK, Bit(False))
	cycle 0
    1: Poke(FIFOGenerator.ARES_design.RESET, Bit(True))
    2: Step(FIFOGenerator.ARES_design.CLK, steps=2)
	cycle 1 
    3: Poke(FIFOGenerator.ARES_design.RESET, Bit(False))
    4: Step(FIFOGenerator.ARES_design.CLK, steps=2)
	cycle 2 
    5: Expect(ARES_design_Empty, Bit(True))
    6: Expect(ARES_design_Full, Bit(False))
    7: Poke(FIFOGenerator.ARES_design.Write, Bit(True))
    8: Poke(FIFOGenerator.ARES_design.WData, 15)
    9: Step(FIFOGenerator.ARES_design.CLK, steps=2)
	cycle 3 
    10: Expect(ARES_design_Empty, Bit(False))
    11: Expect(ARES_design_Full, Bit(False))
    12: Poke(FIFOGenerator.ARES_design.Write, Bit(True))
    13: Poke(FIFOGenerator.ARES_design.WData, 16)
    14: Step(FIFOGenerator.ARES_design.CLK, steps=2)
	cycle 4
    15: Expect(ARES_design_Empty, Bit(False))
    16: Expect(ARES_design_Full, Bit(False))
    17: Poke(FIFOGenerator.ARES_design.Write, Bit(True))
    18: Poke(FIFOGenerator.ARES_design.WData, 17)
    19: Step(FIFOGenerator.ARES_design.CLK, steps=2)
	cycle 5 
    20: Expect(ARES_design_Empty, Bit(False))
    21: Expect(ARES_design_Full, Bit(False))
    22: Poke(FIFOGenerator.ARES_design.Write, Bit(True))
    23: Poke(FIFOGenerator.ARES_design.WData, 18)
    24: Step(FIFOGenerator.ARES_design.CLK, steps=2)
	cycle 6 
    25: Expect(ARES_design_Empty, Bit(False))
    26: Expect(ARES_design_Full, Bit(True))
    27: Poke(FIFOGenerator.ARES_design.Write, Bit(False))
    28: Expect(ARES_design_RData, 15)
    29: Poke(FIFOGenerator.ARES_design.Read, Bit(True))
    30: Step(FIFOGenerator.ARES_design.CLK, steps=2)
	cycle 7 
    31: Expect(ARES_design_Empty, Bit(False))
    32: Expect(ARES_design_Full, Bit(False))
    33: Expect(ARES_design_RData, 16)
    34: Poke(FIFOGenerator.ARES_design.Read, Bit(True))
    35: Step(FIFOGenerator.ARES_design.CLK, steps=2)
	cycle 8 
    36: Expect(ARES_design_Empty, Bit(False))
    37: Expect(ARES_design_Full, Bit(False))
    38: Expect(ARES_design_RData, 17)
    39: Poke(FIFOGenerator.ARES_design.Read, Bit(True))
    40: Step(FIFOGenerator.ARES_design.CLK, steps=2)
	cycle 9 
    41: Expect(ARES_design_Empty, Bit(False))
    42: Expect(ARES_design_Full, Bit(False))
    43: Expect(ARES_design_RData, 18)
    44: Poke(FIFOGenerator.ARES_design.Read, Bit(True))
    45: Step(FIFOGenerator.ARES_design.CLK, steps=2)
	cycle 10 
    46: Expect(ARES_design_Empty, Bit(True))
    47: Expect(ARES_design_Full, Bit(False))
    48: Poke(FIFOGenerator.ARES_design.Read, Bit(False))
    49: Step(FIFOGenerator.ARES_design.CLK, steps=2)
"""



tester.compile_and_run(target="verilator", magma_output="coreir-verilog",magma_opts={"verilator_debug": True},flags=["--trace"])
#tester.compile_and_run(target="verilator", magma_output="coreir-verilog")

#以下方式，可以生成SV文件
tester.compile_and_run("system-verilog", simulator="vivado", flags=["-Wno-fatal", "--trace"], directory="build")
