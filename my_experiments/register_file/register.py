import math
import magma as m
import mantle

from typing import List, Union, Tuple

#https://github.com/leonardt/magma_register_file_tutorial/blob/master/1-Register%20File%20Example.ipynb
#{{{
#[1]
class Register:
#{{{
    def __init__(self, name: str, init: int=0, has_ce: bool=False):
        self.name = name
        self.init = init
        self.has_ce = has_ce
#}}}

#[2]
def APBBase(addr_width: int, data_width: int):
#{{{
    return {
        "PCLK"   : m.Out(m.Clock),
        "PRESETn": m.Out(m.Reset),
        "PADDR"  : m.Out(m.Bits[addr_width]),
        "PPROT"  : m.Out(m.Bit),
        "PENABLE": m.Out(m.Bit),
        "PWRITE" : m.Out(m.Bit),
        "PWDATA" : m.Out(m.Bits[data_width]),
        # One write strobe bit for each byte of the data bus
        "PSTRB"  : m.Out(m.Bits[math.ceil(data_width / 8)]),
        "PREADY" : m.In(m.Bit),
        "PRDATA" : m.In(m.Bits[data_width]),
        "PSLVERR": m.In(m.Bit),
    }
#}}}

def APBMaster(addr_width: int, data_width: int, num_sel: int=1):
#{{{
    if not data_width <= 32:
        raise ValueError("AMBA 3 APB specifies that the data bus " \
                         "cannot be wider than 32 bits")
    
    fields = {}
    for i in range(num_sel):
        fields[f"PSEL{i}"] = m.Out(m.Bit)
 
    fields.update
        
    fields.update(APBBase(addr_width, data_width))
    
    return m.Product.from_fields("APBMaster", fields)
#}}}

def APBSlave(addr_width: int, data_width: int, slave_id_or_ids: Union[int, List[int]]):
#{{{
    if isinstance(slave_id_or_ids, int):
        slave_id_or_ids = [slave_id_or_ids]
    elif not isinstance(slave_id_or_ids, list) and \
         all(isinstance(x, int) for x in slave_or_slave_ids):
        raise ValueError(f"Received incorrect parameter for "
                         f"`slave_or_slave_ids`: {slave_or_slave_ids}")
    
    fields = {f"PSEL{slave_id}": m.Out(m.Bit) for slave_id in slave_id_or_ids}
    fields.update(APBBase(addr_width, data_width))
    
    return m.Product.from_fields("APBSlave", fields).flip()
#}}}

#[5]
def make_reg_file_interface(reg_list: Tuple[Register], data_width: int, apb_slave_id: int):
#{{{
    addr_width = m.bitutils.clog2(len(reg_list)) 
    Data = m.Bits[data_width]
    
    #m.IO的定义暂时不知道，不过后面的port_name叫“apb”，是按照这个apb来的
    #我改叫apb_1，后面也能变
    #但是为了照顾后面的RegisterFileGenerator，里面有个PSEL = getattr(io.apb, f"PSEL{apb_slave_id}") 所以不能改名
    #这个reg_file_interface一定有一个APBSlave，然后才是reg_list里那些reg

    io = m.IO(apb=APBSlave(addr_width, data_width, apb_slave_id))
    for reg in reg_list:
        io += m.IO(**{f"{reg.name}_d": m.In(Data)})
        if reg.has_ce:
            io += m.IO(**{f"{reg.name}_en": m.In(m.Enable)})
        io += m.IO(**{f"{reg.name}_q": m.Out(Data)})
    return io
#}}}

#[7]
class RegisterFileGenerator(m.Generator2):
#{{{
    #构造函数
    def __init__(self, regs, data_width, apb_slave_id=0):
        #起名，用到regs的信息
        self.name = "RegFile_" + "_".join(reg.name for reg in regs)
        
        self.io = io = make_reg_file_interface(regs, data_width, apb_slave_id)

        for name, port in io.ports.items():
            print(f"port_name = \"{name}\"")
            print(f"port_type = ", end="")
            m.util.pretty_print_type(type(port))
            print()


        PSEL = getattr(io.apb, f"PSEL{apb_slave_id}")
        
        #这里又用了mantle.Register，这个东西能声明成design内部的reg，有五个signal，I,O,CLK,CE,RESET
		#所以有了后面的reg.I怎么怎么样
        registers = [
            mantle.Register(data_width, init=reg.init, has_ce=True,
                            has_reset=True, name=reg.name)
            for reg in regs
        ]
        #is_write应该是一个内部的状态
        is_write = io.apb.PENABLE & io.apb.PWRITE & PSEL

        ready = None
        for i, reg in enumerate(registers):
            reg.I @= mantle.mux([getattr(io, reg.name + "_d"),
                                 io.apb.PWDATA], is_write)

            getattr(io, reg.name + "_q") <= reg.O

            reg.CLK @= io.apb.PCLK
            reg.RESET @= ~m.bit(io.apb.PRESETn)

            ce = is_write & (io.apb.PADDR == i)
            if regs[i].has_ce:
                reg.CE @= ce | m.bit(getattr(io, reg.name + "_en"))
            else:
                reg.CE @= ce

            if ready is not None:
                ready |= ce
            else:
                ready = ce

        is_read = io.apb.PENABLE & ~io.apb.PWRITE & PSEL

        io.apb.PREADY @= ready | is_read

        io.apb.PRDATA @= mantle.mux(
            [reg.O for reg in registers], io.apb.PADDR)

        io.apb.PSLVERR.undriven()
        io.apb.PPROT.unused()
        io.apb.PSTRB.unused()
#}}}

#RUN
#=========================================================================
#[3]
#APBMaster_obj = APBMaster(addr_width=16, data_width=32, num_sel=2)
#m.util.pretty_print_type(APBMaster_obj)

#[4]
#APBSlave_obj = APBSlave(addr_width=16, data_width=32, slave_id_or_ids=[0, 1])
#m.util.pretty_print_type(APBSlave_obj)

#[6]
#interface = make_reg_file_interface(reg_list=[Register("reg0", 1, True), Register("reg1", 24)], data_width=32, apb_slave_id=1)
#interface里有两个register，reg_0 bit为1，有ce，reg_1 bit为24,无ce
"""
for name, port in interface.ports.items():
    print(f"port_name = \"{name}\"")
    print(f"port_type = ", end="")
    m.util.pretty_print_type(type(port))
    print()
"""

#[8]
RegFile = RegisterFileGenerator((Register("reg0", 1, True), Register("reg1", 24)), data_width=32, apb_slave_id=1)

#print(repr(RegFile))
m.compile("build/RegFile", RegFile)





#}}}
