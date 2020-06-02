import magma as m
import mantle
from hwtypes import  Product



def make_FIFO(data_type, depth):
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
		#return m.Flip(interface)
		return interface

	class FIFO(m.Circuit):
		interface = make_HandshakeData(data_type)

		io = m.IO(FIFO_design = interface)
		#io += m.ClockIO()
		
		addr_width = m.bitutils.clog2(depth)
		buffer = mantle.RAM(2**addr_width, io.FIFO_design.WData.flat_length())
		
		buffer.WDATA @= m.as_bits(io.FIFO_design.WData)
		io.FIFO_design.RData @= buffer.RDATA
		
		read_pointer = mantle.Register(addr_width + 1)
		write_pointer = mantle.Register(addr_width + 1)
		buffer.RADDR @= read_pointer.O[:addr_width]
		buffer.WADDR @= write_pointer.O[:addr_width]
		
		reset = io.FIFO_design.RESET

		full = \
			(read_pointer.O[:addr_width] == write_pointer.O[:addr_width]) \
			& \
			(read_pointer.O[addr_width] != write_pointer.O[addr_width])
		
		empty = read_pointer.O == write_pointer.O
		write_valid = io.FIFO_design.Write & ~full
		read_valid = io.FIFO_design.Read & ~empty
	
		io.FIFO_design.Full @= full
		
		buffer.WE @= write_valid

		write_p = mantle.mux([
			write_pointer.O, m.uint(write_pointer.O) + 1
		], write_valid)
		
		write_pointer.I @= mantle.mux([
			write_p, 0
		], reset)
	
		io.FIFO_design.Empty @= empty
		
		read_p = mantle.mux([
			read_pointer.O, m.uint(read_pointer.O) + 1
		], read_valid)

		read_pointer.I @= mantle.mux([
			read_p, 0 
		], reset)

	return FIFO



#FIFO = make_FIFO(m.UInt[32], 4)

#m.compile("build/my_FIFO", FIFO, output="coreir-verilog")

