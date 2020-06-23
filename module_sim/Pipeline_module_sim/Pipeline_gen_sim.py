import magma as m
import mantle
import fault
import sys

from typing import List, Union, Tuple
from hwtypes import Enum, Product, Bit, BitVector

import pprint
pp = pprint.PrettyPrinter()

from turing_old.src.rtl.DesignLib.Pipeline import Pipeline
#from turing_old.src.rtl.DesignLib.Fifo import Fifo
#from turing_old.src.rtl.DesignLib.Register import Register

def Pipeline_declare (depth = 4):
	PIPELINE = Pipeline.generate(m.Bits[32], depth)
	return PIPELINE

def tester_reset (tester):
	#On VCS sim part, the initial clk status is low. So all even step are clk negedge, odd step are clk posedge
	tester.circuit.clocks.resetn = 0
	tester.circuit.I = 0
	tester.circuit.CE = 0
	tester.step(2)

	tester.circuit.clocks.resetn = 1 
	tester.step(2)


def Pipeline_test (tester, depth = 4): 
#{{{
	base_write_data = 10

	loop_count = 5 

	#NOTE:
	#Even through I may not want to write data into I, I still need to rise CE, because I need to keep pushing data to the front (O).
	#I tried to only input depth*(loop_count - 1) data and expect O part to show all these data, but the last data cannot be read, because the last data (number depth*(loop_count - 1) data) is not pushed to the front (O). 

	for i in range (0, depth * loop_count):
		tester.circuit.I = base_write_data + i
		tester.circuit.CE = 1

		if i >= depth:
			tester.circuit.O.expect(base_write_data + i - depth)

		tester.step(2)
	
	#print (tester)
#}}}


depth = 16 
mode = 3
try:
	mode = int (sys.argv[1])
except:
	print ("Run default mode 3.")

try:
	depth = int(sys.argv[2])
except:
	print ("Use default depth = 16.")



Pipeline = Pipeline.generate(m.Bits[32], depth)

if mode == 1:
	#ONE: this is generate verilog code only
	m.compile("build/my_Pipeline", Pipeline, inline="True", output="coreir-verilog")

if mode == 2:
	#TWO: This is fault test, if not match expect, fault will report error
	tester = fault.Tester(Pipeline, clock=Pipeline.clocks.clk)
	tester_reset(tester)
	Pipeline_test (tester, depth)
	tester.compile_and_run(target="verilator", magma_output="coreir-verilog",magma_opts={"verilator_debug": True},flags=["--trace"])

if mode == 3:
	#THREE: This is vcs test, if not match expect, fault will not report error, but vcs will report
	tester = fault.Tester(Pipeline, clock=Pipeline.clocks.clk)
	tester_reset(tester)
	Pipeline_test (tester, depth)
	tester.compile_and_run("system-verilog", simulator="vcs", flags=["-Wno-fatal", "--trace"], directory="build")






