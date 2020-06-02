#https://github.com/leonardt/magma_register_file_tutorial/blob/master/4-Using%20the%20Register%20File.ipynb

import math
import magma as m
import mantle
import APB
import verify_register 
import register
import fault
import logging
import sys

from typing import List, Union, Tuple
from hwtypes import BitVector
from hwtypes import Bit

#[3]
class DMA(m.Circuit):
    """
    Stub DMA module
    """
    io = m.IO(csr=m.In(m.Bits[32]), src_addr=m.In(m.Bits[32]),
              dst_addr=m.In(m.Bits[32]), txfr_len=m.In(m.Bits[32]))

    io.csr.unused()
    io.src_addr.unused()
    io.dst_addr.unused()
    io.txfr_len.unused()

#[4]
class TopGenerator(m.Generator2):
    def __init__(self, mode="pack"):
        """
        Simple example that instances two stub DMA modules and is paramtrizable
        over distributed versus packed register file
        """
        
        if mode not in ["pack", "distribute"]:
            raise ValueError(f"Unexpected mode {mode}")

        fields = ["csr", "src_addr", "dst_addr", "txfr_len"]
        data_width = 32
        if mode == "pack":
            addr_width = math.ceil(math.log2(len(fields) * 2))
        else:
            addr_width = math.ceil(math.log2(len(fields)))

        self.name = "Top_" + mode
        if mode == "pack":
            self.io = io = m.IO(apb=register.APBSlave(addr_width, data_width, 0))
        else:
            self.io = io = m.IO(apb=register.APBSlave(addr_width, data_width, [0, 1]))

        dmas = [DMA(name=f"dma{i}") for i in range(2)]
        if mode == "pack":
            regs = tuple(register.Register(name + str(i)) for i in range(2) for name in fields)
            reg_file = register.RegisterFileGenerator(regs, data_width=32)(name="reg_file")
            for i in range(2):
                for name in fields:
                    m.wire(getattr(reg_file, name + str(i) + "_q"),
                           getattr(dmas[i], name))
            m.wire(io.apb, reg_file.apb)
            for i in range(2):
                for name in fields:
                    m.wire(getattr(reg_file, name + str(i) + "_q"),
                           getattr(reg_file, name + str(i) + "_d"))
        else:
            apb_outputs = {}
            for key, type_ in APB.APBBase(addr_width, data_width).items():
                if type_.is_input():
                    apb_outputs[key] = []
            for i in range(2):
                regs = tuple(register.Register(name) for name in fields)
                reg_file = register.RegisterFileGenerator(
                    regs, data_width=32, apb_slave_id=i
                )(name=f"reg_file{i}")
                for name in fields:
                    m.wire(getattr(reg_file, name + "_q"),
                           getattr(dmas[i], name))
                for key, type_ in APB.APBBase(addr_width, data_width).items():
                    if type_.is_output():
                        m.wire(getattr(io.apb, key),
                               getattr(reg_file.apb, key))
                    else:
                        apb_outputs[key].append(getattr(reg_file.apb, key))
                m.wire(getattr(io.apb, f"PSEL{i}"),
                       getattr(reg_file.apb, f"PSEL{i}"))
                for name in fields:
                    m.wire(getattr(reg_file, name + "_q"),
                           getattr(reg_file, name + "_d"))
            for key, values in apb_outputs.items():
                m.wire(getattr(io.apb, key),
                       mantle.mux(values, io.apb.PSEL1))

dma_fields = ["csr", "src_addr", "dst_addr", "txfr_len"]

#[5]
def test_top_simple_write(mode, num_slaves):
#{{{
    Top = TopGenerator(mode=mode)
    print(Top, mode)

    tester = fault.Tester(Top, clock=Top.apb.PCLK)
    tester.circuit.apb.PRESETn = 1

    addr_width = len(Top.apb.PADDR)
    data_width = len(Top.apb.PWDATA)
    bus = APB.APBBus(addr_width, data_width, num_slaves)
    for i in range(2):
        for addr, field in enumerate(dma_fields):
            if mode == "pack":
                addr += i * len(dma_fields)
                slave_id = 0
            else:
                slave_id = i
            data = fault.random.random_bv(data_width)
            io, request = verify_register.make_request(addr, data, addr_width, data_width, num_slaves, slave_id)

            verify_register.write(bus, io, request, tester, addr, data)
            if mode == "pack":
                getattr(tester.circuit.reg_file, f"{field}{i}_q").expect(data)
            else:
                getattr(getattr(tester.circuit, f"reg_file{i}"),f"{field}_q").expect(data)
            getattr(getattr(tester.circuit, f"dma{i}"),f"{field}").expect(data)

    tester.compile_and_run(target="verilator", magma_output="coreir-verilog", magma_opts={"verilator_debug": True})
#}}}

#RUN
#[2]
"""
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create STDERR handler
handler = logging.StreamHandler(sys.stderr)

# Create formatter and add it to the handler
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Set STDERR handler as the only handler 
logger.handlers = [handler]


#[6]
test_top_simple_write("pack", 1)
"""

my_design= TopGenerator()
m.compile("build/my_design", my_design)
