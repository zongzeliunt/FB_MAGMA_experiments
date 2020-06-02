#https://github.com/leonardt/magma_register_file_tutorial/blob/master/3-Verifying%20The%20Register%20File.ipynb
#笔记：
#1）[4]步里，那个reset设为true先不要comment，因为教程里是36步，包括了那个reset那步
#2) [8]和[13]那两个write和read的手段是：
	#io里有request，每次改变request的状态来改变io的信号的值。然后call step.
	#	1. 用step把io的信号值给bus，
	#	2. 把bus连给tester。
	#	3. tester.step(2) 可能是过两个cycle
	#	4. tester.circuit.apb.PREADY.expect(1) 这个东西的意思是，我已经执行了几个cycle了，现在我期待看到信号PREADY的值是1
	#	5. tester.compile_and_run(target="verilator", magma_output="coreir-verilog",flags=["-Wno-UNUSED", "-Wno-UNDRIVEN"])
	#		执行这个的意思就是让tester跑起来，参数是干什么的暂时不明确，不过能生成.v文件，也能把那些步骤都走一遍，假如某步的expect值和真实信号的值不同，跑的结果会报错。

import math
import magma as m
import mantle
import APB
import register
import fault
import logging
import sys

from typing import List, Union, Tuple
from hwtypes import BitVector
from hwtypes import Bit



#[7]
def make_request(addr, data, addr_width, data_width, num_slaves=1, slave_id=0):
#{{{
    #最后返回的io里包括了request，也就是说，如果改变了request的值，是可以改动io的
    request = APB.Request(addr_width, data_width, num_slaves)(
        APB.APBCommand.IDLE, BitVector[addr_width](addr),
        BitVector[data_width](data),
        BitVector[max(math.ceil(math.log2(num_slaves)), 1)](slave_id))

    # Specialized instance of APB for addr/data width
    _APB = APB.APB(addr_width, data_width, num_slaves)

    io = APB.APBBusIO(addr_width, data_width, num_slaves)(APB.default_APB_instance(_APB), request)
    return io, request
#}}}

#[8]
def set_apb_inputs(tester, bus):
#{{{
    for key in tester._circuit.apb.keys():
        # Skip clock signals
        if key in ["PCLK", "PRESETn"]:
            continue
        if tester._circuit.apb[key].is_output():
            setattr(tester.circuit.apb, key, getattr(bus.io.apb, key))
#}}}

def step(bus, io, tester):
#{{{
    bus(io)
    set_apb_inputs(tester, bus)
    tester.step(2)
#}}}

def write(bus, io, request, tester, addr, data):
#{{{
    #{{{
    #0: Poke(RegFile_reg0_reg1.apb.PCLK, Bit(False))
    #1: Poke(RegFile_reg0_reg1.apb.PRESETn, Bit(True))
    #2: Poke(RegFile_reg0_reg1.apb.PSEL1, Bit(False))
    #3: Poke(RegFile_reg0_reg1.apb.PADDR, 0)
    #4: Poke(RegFile_reg0_reg1.apb.PPROT, Bit(False))
    #5: Poke(RegFile_reg0_reg1.apb.PENABLE, Bit(False))
    #6: Poke(RegFile_reg0_reg1.apb.PWRITE, Bit(False))
    #7: Poke(RegFile_reg0_reg1.apb.PWDATA, 0)
    #8: Poke(RegFile_reg0_reg1.apb.PSTRB, 0)
    #9: Step(RegFile_reg0_reg1.apb.PCLK, steps=2)
    #10: Poke(RegFile_reg0_reg1.apb.PSEL1, Bit(True))
    #11: Poke(RegFile_reg0_reg1.apb.PADDR, 1)
    #12: Poke(RegFile_reg0_reg1.apb.PPROT, Bit(False))
    #13: Poke(RegFile_reg0_reg1.apb.PENABLE, Bit(False))
    #14: Poke(RegFile_reg0_reg1.apb.PWRITE, Bit(True))
    #15: Poke(RegFile_reg0_reg1.apb.PWDATA, 45)
    #16: Poke(RegFile_reg0_reg1.apb.PSTRB, 0)
    #17: Step(RegFile_reg0_reg1.apb.PCLK, steps=2)
    #18: Poke(RegFile_reg0_reg1.apb.PSEL1, Bit(True))
    #19: Poke(RegFile_reg0_reg1.apb.PADDR, 1)
    #20: Poke(RegFile_reg0_reg1.apb.PPROT, Bit(False))
    #21: Poke(RegFile_reg0_reg1.apb.PENABLE, Bit(True))
    #22: Poke(RegFile_reg0_reg1.apb.PWRITE, Bit(True))
    #23: Poke(RegFile_reg0_reg1.apb.PWDATA, 45)
    #24: Poke(RegFile_reg0_reg1.apb.PSTRB, 0)
    #25: Step(RegFile_reg0_reg1.apb.PCLK, steps=2)
    #26: Expect(apb_PREADY, Bit(True))
    #27: Poke(RegFile_reg0_reg1.apb.PSEL1, Bit(False))
    #28: Poke(RegFile_reg0_reg1.apb.PADDR, 1)
    #29: Poke(RegFile_reg0_reg1.apb.PPROT, Bit(False))
    #30: Poke(RegFile_reg0_reg1.apb.PENABLE, Bit(False))
    #31: Poke(RegFile_reg0_reg1.apb.PWRITE, Bit(True))
    #32: Poke(RegFile_reg0_reg1.apb.PWDATA, 45)
    #33: Poke(RegFile_reg0_reg1.apb.PSTRB, 0)
    #34: Step(RegFile_reg0_reg1.apb.PCLK, steps=2)
    #35: Expect(apb_PREADY, Bit(False))
    #36: Step(RegFile_reg0_reg1.apb.PCLK, steps=2)
    #}}}

    #0和1,clk和reset 在外面已经写了

	#2到9
    step(bus, io, tester)

    # Send request
    #10到17
    request.command = APB.APBCommand.WRITE
    step(bus, io, tester)

    #18到25
    
    request.command = APB.APBCommand.IDLE

    # No wait state
    io.apb.PREADY = Bit(1)
    step(bus, io, tester)

    #26: Expect(apb_PREADY, Bit(True))
    tester.circuit.apb.PREADY.expect(1)
    #27到34
    step(bus, io, tester)
    
    #35 到36
    #35: Expect(apb_PREADY, Bit(False))
    #36: Step(RegFile_reg0_reg1.apb.PCLK, steps=2)
    tester.circuit.apb.PREADY.expect(0)
    tester.step(2)
#}}}

#[13]
def read(bus, io, request, tester, addr, data):
    #{{{
    #36: Poke(RegFile_reg0_reg1.apb.PSEL1, Bit(True))
    #37: Poke(RegFile_reg0_reg1.apb.PADDR, 1)
    #38: Poke(RegFile_reg0_reg1.apb.PPROT, Bit(False))
    #39: Poke(RegFile_reg0_reg1.apb.PENABLE, Bit(False))
    #40: Poke(RegFile_reg0_reg1.apb.PWRITE, Bit(False))
    #41: Poke(RegFile_reg0_reg1.apb.PWDATA, 45)
    #42: Poke(RegFile_reg0_reg1.apb.PSTRB, 0)
    #43: Step(RegFile_reg0_reg1.apb.PCLK, steps=2)
    #44: Poke(RegFile_reg0_reg1.apb.PSEL1, Bit(True))
    #45: Poke(RegFile_reg0_reg1.apb.PADDR, 1)
    #46: Poke(RegFile_reg0_reg1.apb.PPROT, Bit(False))
    #47: Poke(RegFile_reg0_reg1.apb.PENABLE, Bit(True))
    #48: Poke(RegFile_reg0_reg1.apb.PWRITE, Bit(False))
    #49: Poke(RegFile_reg0_reg1.apb.PWDATA, 45)
    #50: Poke(RegFile_reg0_reg1.apb.PSTRB, 0)
    #51: Step(RegFile_reg0_reg1.apb.PCLK, steps=2)
    #52: Expect(apb_PREADY, Bit(True))
    #53: Expect(apb_PRDATA, 45)
    #54: Poke(RegFile_reg0_reg1.apb.PSEL1, Bit(False))
    #55: Poke(RegFile_reg0_reg1.apb.PADDR, 1)
    #56: Poke(RegFile_reg0_reg1.apb.PPROT, Bit(False))
    #57: Poke(RegFile_reg0_reg1.apb.PENABLE, Bit(False))
    #58: Poke(RegFile_reg0_reg1.apb.PWRITE, Bit(False))
    #59: Poke(RegFile_reg0_reg1.apb.PWDATA, 45)
    #60: Poke(RegFile_reg0_reg1.apb.PSTRB, 0)
    #61: Step(RegFile_reg0_reg1.apb.PCLK, steps=2)
    #62: Expect(apb_PREADY, Bit(False))
    #63: Step(RegFile_reg0_reg1.apb.PCLK, steps=2)
    #}}}



    # Send request
    #36 到 43
    request.command = APB.APBCommand.READ
    step(bus, io, tester)
    
    #44 到 51
    request.command = APB.APBCommand.IDLE

    # No wait state
    io.apb.PREADY = Bit(1)
    step(bus, io, tester)

    #52: Expect(apb_PREADY, Bit(True))
    tester.circuit.apb.PREADY.expect(1)
    #53: Expect(apb_PRDATA, 45)
    tester.circuit.apb.PRDATA.expect(data)
    #54 到 61
    step(bus, io, tester)

    #62: Expect(apb_PREADY, Bit(False))
    tester.circuit.apb.PREADY.expect(0)
    tester.step(2)


#RUN
#=====================================================

#[2]                           
RegFile = register.RegisterFileGenerator((register.Register("reg0", 1, True), register.Register("reg1", 24)), data_width=32, apb_slave_id=1)

#[3]
tester = fault.Tester(RegFile, clock=RegFile.apb.PCLK)

#用这种方式 可以在这里随便安排信号的值
#[4]
tester.circuit.apb.PRESETn = 1
#tester.circuit.apb.PRESETn = 0 
#[5]
#print(tester)

#[6]
addr_width = 1
data_width = 32
addr = 1
data = 45
bus = APB.APBBus(addr_width, data_width, num_slaves=2)
io, request = make_request(addr, data, addr_width, data_width, num_slaves=2, slave_id=1)

#[8]
#io 包括了request，在write的step里，把io输给了bus
#write(bus, io, request, tester, addr, data)

#[9]
#print(tester)

#[10]
#getattr(tester.circuit, f"reg{addr}_q").expect(data)

#[11]
#tester.compile_and_run(target="verilator", magma_output="coreir-verilog", flags=["-Wno-UNUSED", "-Wno-UNDRIVEN"])


#[12]
"""
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

tester.compile_and_run(target="verilator", magma_output="coreir-verilog", flags=["-Wno-UNUSED", "-Wno-UNDRIVEN"])
"""

#[13]
"""
tester.clear()
tester.circuit.apb.PRESETn = 1

io, request = make_request(addr, data, addr_width, data_width, num_slaves=2,slave_id=1)

write(bus, io, request, tester, addr, data)

read(bus, io, request, tester, addr, data)

#print (tester)
tester.compile_and_run(target="verilator", magma_output="coreir-verilog",flags=["-Wno-UNUSED", "-Wno-UNDRIVEN"])
"""

#[14]
tester.clear()
tester.circuit.apb.PRESETn = 1

values = ((0xDE, 0xAD), (0xBE, 0xEF))
for i in range(2):
    for addr, data in enumerate(values[i]):
        io, request = make_request(addr, data, addr_width, data_width, num_slaves=2, slave_id=1)
        write(bus, io, request, tester, addr, data)
        getattr(tester.circuit, f"reg{addr}_q").expect(data)

    for addr, data in enumerate(values[i]):
        io, request = make_request(addr, data, addr_width, data_width, num_slaves=2, slave_id=1)
        read(bus, io, request, tester, addr, data)

tester.compile_and_run(target="verilator", magma_output="coreir-verilog",
                       flags=["-Wno-UNUSED", "-Wno-UNDRIVEN"])
