import magma as m
import mantle
from hwtypes import  Product

#这里有两个版本的声明FIFO的方式，有用class和函数，函数其实也是class
#	只有在函数版本里才能用	m.Circuit，class版本必须用m.Generator2否则报错
#		raise Exception("Can not instance a circuit outside a definition")
#	class版本得有个构造函数__init__，否则外面的参数变量不知道怎么传进来	
#	class版本可以不设self.name,这样module name就是默认的FIFOGenerator

def make_HandshakeData(data_type):
	interface = m.Product.from_fields("HandshakeData", {
		"CLK"  : m.In (m.Clock),
        "RESET"  : m.In (m.Reset),
		"WData": m.In (data_type),
		"Full":  m.Out(m.Bit),
		"Write": m.In (m.Bit),
		"RData": m.Out(data_type),
		"Empty": m.Out(m.Bit),
		"Read":  m.In (m.Bit)
	})
	return interface 


#这个是函数版本的
def make_FIFO(ARES_design_type, depth):
#{{{
	class FIFO(m.Circuit):
		io = m.IO(ARES_design = ARES_design_type)
		#io += m.ClockIO()
		
		addr_width = m.bitutils.clog2(depth)
		buffer = mantle.RAM(2**addr_width, io.ARES_design.WData.flat_length())
		
		buffer.WDATA @= m.as_bits(io.ARES_design.WData)
		io.ARES_design.RData @= buffer.RDATA
		
		read_pointer = mantle.Register(addr_width + 1)
		write_pointer = mantle.Register(addr_width + 1)
		buffer.RADDR @= read_pointer.O[:addr_width]
		buffer.WADDR @= write_pointer.O[:addr_width]
		
		reset = io.ARES_design.RESET

		full = \
			(read_pointer.O[:addr_width] == write_pointer.O[:addr_width]) \
			& \
			(read_pointer.O[addr_width] != write_pointer.O[addr_width])
		
		empty = read_pointer.O == write_pointer.O
		write_valid = io.ARES_design.Write & ~full
		read_valid = io.ARES_design.Read & ~empty
	
		io.ARES_design.Full @= full
		
		buffer.WE @= write_valid

		write_p = mantle.mux([
			write_pointer.O, m.uint(write_pointer.O) + 1
		], write_valid)
		
		write_pointer.I @= mantle.mux([
			write_p, 0
		], reset)
	
		io.ARES_design.Empty @= empty
		
		read_p = mantle.mux([
			read_pointer.O, m.uint(read_pointer.O) + 1
		], read_valid)

		read_pointer.I @= mantle.mux([
			read_p, 0 
		], reset)


			


	return FIFO
#}}}

#这个是class版本的,仿register.py

class FIFOGenerator(m.Generator2):
#{{{
	def __init__(self, ARES_design_type, depth):
		#这个self.name 和self.io必须得有
		#self.name = "ARES_FIFO_DESIGN"
		self.io = io = m.IO(ARES_design = ARES_design_type)
		#io += m.ClockIO()
		
		addr_width = m.bitutils.clog2(depth)
		print ("ARES addr width : " + str(addr_width) )
		buffer = mantle.RAM(2**addr_width, io.ARES_design.WData.flat_length())
		
		buffer.WDATA @= m.as_bits(io.ARES_design.WData)
		io.ARES_design.RData @= buffer.RDATA
		
		read_pointer = mantle.Register(addr_width + 1)
		write_pointer = mantle.Register(addr_width + 1)
		buffer.RADDR @= read_pointer.O[:addr_width]
		buffer.WADDR @= write_pointer.O[:addr_width]
		
		reset = io.ARES_design.RESET

		full = \
			(read_pointer.O[:addr_width] == write_pointer.O[:addr_width]) \
			& \
			(read_pointer.O[addr_width] != write_pointer.O[addr_width])
		
		empty = read_pointer.O == write_pointer.O
		write_valid = io.ARES_design.Write & ~full
		read_valid = io.ARES_design.Read & ~empty
	
		io.ARES_design.Full @= full
		
		buffer.WE @= write_valid

		write_p = mantle.mux([
			write_pointer.O, m.uint(write_pointer.O) + 1
		], write_valid)
		
		write_pointer.I @= mantle.mux([
			write_p, 0
		], reset)
	
		io.ARES_design.Empty @= empty
		
		read_p = mantle.mux([
			read_pointer.O, m.uint(read_pointer.O) + 1
		], read_valid)

		read_pointer.I @= mantle.mux([
			read_p, 0 
		], reset)
#}}}




#RUN
#==================================
interface = make_HandshakeData(m.UInt[32])
#函数版本
#FIFO = make_FIFO(interface, 4)
#class版本
FIFO = FIFOGenerator(interface, 4)




m.compile("build/my_FIFO", FIFO, output="coreir-verilog")

