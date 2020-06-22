import magma as m
import mantle
from hwtypes import  Product




def make_AXI(data_type, depth):
	def make_HandshakeData(data_type):
		interface = m.Product.from_fields("HandshakeData", {
			"CLK"  			: m.In 	(m.Clock),
			"RESET"  		: m.In 	(m.Reset),
			"WReq_valid"	: m.In 	(m.Bit),
			"WReq_ready"	: m.Out (m.Bit),
			"WReq_size"		: m.In 	(data_type),
			"WReq_addr"		: m.In 	(data_type),
			"W_valid"		: m.In	(m.Bit),
			"W_ready"		: m.Out (m.Bit),
			"W_data"		: m.In	(data_type),
			"RReq_valid"	: m.In 	(m.Bit),
			"RReq_ready"	: m.Out (m.Bit),
			"RReq_size"		: m.In 	(data_type),
			"RReq_addr"		: m.In 	(data_type),
			"R_valid"		: m.Out	(m.Bit),
			"R_ready"		: m.In  (m.Bit),
			"R_data"		: m.Out	(data_type),
		})
		return interface


 
	class AXI(m.Circuit):
		interface = make_HandshakeData(data_type)
		io = m.IO(ARES_design = interface)
		
		addr_width = m.bitutils.clog2(depth)

		reset = io.ARES_design.RESET
	
		#data_buffer	
		#===============================================================

		buffer = mantle.RAM(2**addr_width, io.ARES_design.W_data.flat_length())

	
		#WReq	操作
		#===============================================================
		WReq_size_reg = mantle.Register(32)
		WReq_addr_reg = mantle.Register(32)
		
		#不要改！ 这个have_WReq_signal 代表我现在有一个WReq要处理
		have_WReq_signal = ~(WReq_size_reg.O == 0)
		#不要改！ 有WReq就不能再接新的了！所以WReq_ready要为0
		io.ARES_design.WReq_ready @= mantle.mux([~have_WReq_signal , 1], reset)

		WReq_valid_signal = io.ARES_design.WReq_valid & ~have_WReq_signal
	
		receive_WReq_size_signal = mantle.mux([m.uint(0, 32), io.ARES_design.WReq_size], WReq_valid_signal)
		receive_WReq_addr_signal = mantle.mux([m.uint(0, 32), io.ARES_design.WReq_addr], WReq_valid_signal)

		#这个是真Write_valid 这个东西的意思就是，我用have_WReq_signal代表W_ready。假如W_valid为1,那就是握手完成
		#本来应该放在Write 操作里的，我放在这里是要reduce WReq_size
		W_valid_signal = io.ARES_design.W_valid & have_WReq_signal

		reduce_WReq_size_signal = mantle.mux([WReq_size_reg.O, m.uint(WReq_size_reg.O) - 1 ], W_valid_signal)
	
		#有WReq则处理size，没有则准备好从外面拿
		WReq_size_signal = mantle.mux([receive_WReq_size_signal, reduce_WReq_size_signal], have_WReq_signal)
		WReq_size_reg.I @= mantle.mux([WReq_size_signal, m.uint(0, 32)] ,reset)

		#有WReq则保留addr，没有则准备好从外面拿
		WReq_addr_signal = mantle.mux([receive_WReq_addr_signal, WReq_addr_reg.O], have_WReq_signal)
		WReq_addr_reg.I @= mantle.mux([WReq_addr_signal, m.uint(0, 32)] ,reset)

		#Write 操作
		#===============================================================
		#W_ready
		io.ARES_design.W_ready @= mantle.mux([have_WReq_signal , 0], reset)

		#W_size_reg
		W_size_reg = mantle.Register(32)
		W_size_reg_increase_signal = mantle.mux([W_size_reg.O, m.uint(W_size_reg.O) + 1], W_valid_signal)
		W_size_signal = mantle.mux([m.uint(0, 32), W_size_reg_increase_signal], have_WReq_signal )

		W_size_reg.I @= mantle.mux([W_size_signal, 0], reset) 
	
		#buffer
		buffer.WDATA @= io.ARES_design.W_data
		buffer.WADDR @= mantle.add(WReq_addr_reg.O[:addr_width], W_size_reg.O[:addr_width])
		
		#have_WReq_signal 就是W_ready，这意味着W_valid和W_ready 同时为1
		buffer.WE 	@= W_valid_signal


		#RReq	操作
		#===============================================================

		RReq_size_reg = mantle.Register(32)
		RReq_addr_reg = mantle.Register(32)
		
		#不要改！ 这个have_RReq_signal 代表我现在有一个WReq要处理
		have_RReq_signal = ~(RReq_size_reg.O == 0)
		#TODO 关于RReq，我现在的办法是从reset起我就能接受RReq，外面随便发读请求，但是读出什么来不好说，大不了就是X
		io.ARES_design.RReq_ready @= mantle.mux([~have_RReq_signal , 1], reset)

		RReq_valid_signal = io.ARES_design.RReq_valid & ~have_RReq_signal
	
		receive_RReq_size_signal = mantle.mux([m.uint(0, 32), io.ARES_design.RReq_size], RReq_valid_signal)
		receive_RReq_addr_signal = mantle.mux([m.uint(0, 32), io.ARES_design.RReq_addr], RReq_valid_signal)



		#这个是真.R_valid。这个东西的意思就是，我用have_RReq_signal代表R_valid。假如R_ready为1,那就是握手完成
		#其实这个信号应该放在Read操作里，但是由于我要用R_valid_signal来让RReq_size减少，所以放在这弄
		R_valid_signal = io.ARES_design.R_ready & have_RReq_signal
		
		#减少RReq_size
		reduce_RReq_size_signal = mantle.mux([RReq_size_reg.O, m.uint(RReq_size_reg.O) - 1 ], R_valid_signal)
	
		#有RReq则处理size，没有则准备好从外面拿
		RReq_size_signal = mantle.mux([receive_RReq_size_signal, reduce_RReq_size_signal], have_RReq_signal)
		RReq_size_reg.I @= mantle.mux([RReq_size_signal, m.uint(0, 32)] ,reset)

		#有RReq则保留addr，没有则准备好从外面拿
		RReq_addr_signal = mantle.mux([receive_RReq_addr_signal, RReq_addr_reg.O], have_RReq_signal)
		RReq_addr_reg.I @= mantle.mux([RReq_addr_signal, m.uint(0, 32)] ,reset)




		#Read操作	
		#===============================================================
		io.ARES_design.R_valid @= mantle.mux([have_RReq_signal , 0], reset)
		
		#R_size_reg
		R_size_reg = mantle.Register(32)
		R_size_reg_increase_signal = mantle.mux([R_size_reg.O, m.uint(R_size_reg.O) + 1], R_valid_signal)
		R_size_signal = mantle.mux([m.uint(0, 32), R_size_reg_increase_signal], have_RReq_signal )

		R_size_reg.I @= mantle.mux([R_size_signal, 0], reset) 


		buffer.RADDR @= mantle.add(RReq_addr_reg.O[:addr_width], R_size_reg.O[:addr_width])
		io.ARES_design.R_data @= buffer.RDATA


	return AXI




AXI = make_AXI(m.UInt[32], 32)

m.compile("build/my_AXI", AXI, output="coreir-verilog")

