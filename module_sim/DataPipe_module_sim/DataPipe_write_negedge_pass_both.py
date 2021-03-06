import magma as m
import mantle
import fault
import sys

from typing import List, Union, Tuple
from hwtypes import Enum, Product, Bit, BitVector

import pprint
pp = pprint.PrettyPrinter()

from turing.src.rtl.DesignLib.DataPipe import DataPipe

def tester_reset (tester):
	#VCS sim, the initial clk status is low. So all even step are clk negedge, odd step are clk posedge
	#Internal signal change at clk posedge, so I need to do my operation on clk negedge to make sure every time I check interface signal on negedge, the status are stable.
	#This is way I cannot use this first tester step
	#=========================== 
	#Do not open this
	#tester.step(1)
	#=========================== 
	tester.circuit.clocks.resetn = 0
	tester.circuit.Din = 0
	tester.circuit.VldIn = 0
	tester.step(2)

	tester.circuit.clocks.resetn = 1 
	tester.step(2)


def DataPipe_test (tester, depth = 4): 
#{{{
	base_write_data = 10
	#Internal signal change at clk posedge, so I need to do my operation on clk negedge to make sure every time I check interface signal on negedge, the status are stable. 
	#tester.step(1)
	loop_count = 2	
	for i in range (0, depth * loop_count):
		tester.circuit.Din = base_write_data + i
		tester.circuit.VldIn = 1
			
		if i < depth:
			tester.circuit.VldOut.expect(0)
		else:
			tester.circuit.VldOut.expect(1)
			tester.circuit.Dout.expect(base_write_data + i - depth)

		tester.step(2)
	tester.circuit.Din = 0 
	tester.circuit.VldIn = 0
		
	tester.step(2)
	
	print (tester)
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


DATAPIPE = DataPipe.generate(m.Bits[32], depth)


if mode == 1:
	#ONE: this is generate verilog code only
	m.compile("build/my_DataPipe", DATAPIPE, inline="True", output="coreir-verilog")

if mode == 2:
	#TWO: This is fault test, if not match expect, fault will report error
	tester = fault.Tester(DATAPIPE, clock=DATAPIPE.clocks.clk)
	tester_reset(tester)
	DataPipe_test (tester, depth)
	
	tester.compile_and_run(
		target="verilator", 
		directory="build",
		magma_output="coreir-verilog",
		magma_opts={"verilator_debug": True},
		flags=["--trace"]
	)

if mode == 3:
	#THREE: This is vcs test, if not match expect, fault will not report error, but vcs will report
	tester = fault.Tester(DATAPIPE, clock=DATAPIPE.clocks.clk)
	tester_reset(tester)
	DataPipe_test (tester, depth)
	tester.compile_and_run(
		"system-verilog", 
		simulator="vcs", 
		flags=["-Wno-fatal", "--trace"], 
		directory="build"
	)






