import magma as m
import mantle
import fault
import sys

from typing import List, Union, Tuple
from hwtypes import Enum, Product, Bit, BitVector

import pprint
pp = pprint.PrettyPrinter()

from turing.src.rtl.DesignLib.Fifo import Fifo

def FIFO_declare (FIFO_depth = 4):
	FIFO = Fifo.generate(m.Bits[32], FIFO_depth)
	return FIFO

def tester_reset (tester):
	#VCS sim, the initial clk status is low. So all even step are clk negedge, odd step are clk posedge
	#Internal signal change at clk posedge, so I need to do my operation on clk negedge to make sure every time I check interface signal on negedge, the status are stable. 
	#This is way I cannot use this first tester step
	#=========================== 
	#Do not open this
	#tester.step(1)
	#=========================== 
	tester.circuit.clocks.resetn = 0
	tester.circuit.dataInValid = 0
	tester.circuit.dataIn = 0
	tester.circuit.dataOutReady = 0
	tester.step(2)

	tester.circuit.clocks.resetn = 1 
	tester.step(2)


def FIFO_test (tester, FIFO_depth = 4): 
#{{{
	base_write_data = 10
	#Internal signal change at clk posedge, so I need to do my operation on clk negedge to make sure every time I check interface signal on negedge, the status are stable. 
	tester.step(1)
	for i in range (0, FIFO_depth):
		if i == 0:
			tester.circuit.dataOutValid.expect(0)
		else:
			tester.circuit.dataOutValid.expect(1)
		tester.circuit.dataInReady.expect(1)
		tester.circuit.dataInValid = True
		tester.circuit.dataIn = base_write_data + i 
		tester.step(2)
		
	for i in range (0, FIFO_depth):
		if i == 0:
			tester.circuit.dataInReady.expect(0)
			tester.circuit.dataInValid = False
			tester.circuit.dataIn = 0 
		else:
			tester.circuit.dataInReady.expect(1)

		tester.circuit.dataOutValid.expect(1)
		tester.circuit.dataOut.expect(base_write_data + i)
		tester.circuit.dataOutReady = True
		tester.step(2)

	
	tester.circuit.dataOutValid.expect(0)
	tester.circuit.dataInReady.expect(1)
	tester.circuit.dataOutReady = False 
	tester.step(2)
	
	#print (tester)
#}}}


depth = 16 
mode = 2 

try:
	mode = int (sys.argv[1])
except:
	print ("Run default mode 2.")

try:
	depth = int(sys.argv[2])
except:
	print ("Use default depth = 16.")

FIFO_depth = depth
FIFO = FIFO_declare (FIFO_depth)
if mode == 1:
	#ONE: this is generate verilog code only
	m.compile("build/my_FIFO", FIFO, inline="True", output="coreir-verilog")

if mode == 2:
	#TWO: This is fault test, if not match expect, fault will report error
	tester = fault.Tester(FIFO, clock=FIFO.clocks.clk)
	tester_reset(tester)
	FIFO_test (tester, FIFO_depth)
	FIFO_test (tester, FIFO_depth)
	tester.compile_and_run(
		target="verilator", 
		directory="build",
		magma_output="coreir-verilog",
		magma_opts={"verilator_debug": True},
		flags=["--trace"]
	)

if mode == 3:
	#THREE: This is vcs test, if not match expect, fault will not report error, but vcs will report
	tester = fault.Tester(FIFO, clock=FIFO.clocks.clk)
	tester_reset(tester)
	FIFO_test (tester, FIFO_depth)
	#FIFO_test (tester, FIFO_depth)
	tester.compile_and_run(
		"system-verilog", 
		simulator="vcs", 
		flags=["-Wno-fatal", "--trace"], 
		directory="build"
	)






