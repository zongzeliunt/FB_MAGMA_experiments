`timescale 1ns/10ps

module AXI_test;
	reg CLK;
	reg RESET;
	reg [31:0] CLK_COUNTER;

	reg [31:0] WReq_addr;
	reg [31:0] WReq_size;
	wire WReq_ready;
	reg WReq_valid;
	
	reg [31:0]WReq_write_count;

	reg [31:0] W_data;
	reg [31:0] W_data_tmp;
	wire W_ready;
	reg W_valid;
	reg W_done;
	
	reg [31:0] RReq_addr;
	reg [31:0] RReq_addr_tmp;
	reg [31:0] RReq_size;
	reg [31:0] RReq_size_tmp;
	wire RReq_ready;
	reg RReq_valid;
	
	reg [31:0]RReq_write_count;

	wire [31:0] R_data;
	reg R_ready;
	wire R_valid;
	

	parameter TB_RESET_VALUE = 1;
	AXI AXI_sim
	(
		.ARES_design_CLK(CLK),
		.ARES_design_RESET(RESET),
		.ARES_design_R_data(R_data),
		.ARES_design_R_ready(R_ready),
		.ARES_design_R_valid(R_valid),
		.ARES_design_RReq_addr(RReq_addr),
		.ARES_design_RReq_size(RReq_size),
		.ARES_design_RReq_ready(RReq_ready),
		.ARES_design_RReq_valid(RReq_valid),
		.ARES_design_W_data(W_data),
		.ARES_design_W_ready(W_ready),
		.ARES_design_W_valid(W_valid),
		.ARES_design_WReq_addr(WReq_addr),
		.ARES_design_WReq_size(WReq_size),
		.ARES_design_WReq_ready(WReq_ready),
		.ARES_design_WReq_valid(WReq_valid)
	);

//WReq
always@(posedge CLK) begin
	if (RESET == TB_RESET_VALUE) begin
		WReq_valid <= 0;
		WReq_write_count <= 32'd0;
		WReq_addr <= 0;
		WReq_size <= 0;
	end
	else begin
		if (WReq_ready == 1 && WReq_write_count == 32'd0) begin
			WReq_size <= 32'd12;
			WReq_addr <= 32'd0;
			WReq_write_count <= WReq_write_count + 32'd1;
			WReq_valid <= 1;
		end
		else begin 
			WReq_valid <= 0;
			WReq_addr <= 0;
			WReq_size <= 0;
		end
	end
end

//W
always@(posedge CLK) begin
	if (RESET == TB_RESET_VALUE) begin
		W_data <= 0;
		W_data_tmp <= 0;
		W_valid <= 0;
		W_done <= 0;
	end
	else begin
		if (W_ready == 1) begin
			if (W_valid == 1) begin
				W_data <= W_data_tmp + 2;
				W_data_tmp <= W_data_tmp + 2;
			end
			else begin
				W_data <= W_data_tmp;
			end
			W_valid <= 1;
		end
		else begin
			W_data <= 0;
			W_valid <=0 ;
		end	
		if (W_data_tmp >= 32'd20) begin
			W_done <= 1;
		end
		
	end
end

//WReq
always@(posedge CLK) begin
	if (RESET == TB_RESET_VALUE) begin
		RReq_valid <= 0;
		RReq_write_count <= 0;
		RReq_addr <= 0;
		RReq_addr_tmp <= 0;
		RReq_size <= 0;
		RReq_size_tmp <= 32'd3;
	end
	else begin
		if (RReq_ready == 1 && W_done == 1 && RReq_write_count <= 32'd2) begin
			RReq_size <= RReq_size_tmp;
			RReq_addr <= RReq_addr_tmp;
			RReq_write_count <= RReq_write_count + 1;
			RReq_valid <= 1;
		end
		else begin 
			RReq_valid <= 0;
		end
		if (RReq_ready == 1 && RReq_valid == 1) begin
			RReq_addr_tmp <= RReq_addr_tmp + RReq_size_tmp;
			RReq_size_tmp <= RReq_size_tmp + 32'd3;
		end
	end
end


//Data_read
always@(posedge CLK) begin
	if (RESET == TB_RESET_VALUE) begin
		R_ready <= 0;
	end
	else begin
		if (R_valid == 1) begin
			R_ready <= 1;
		end
		else begin
			R_ready <= 0;
		end
	end	
end

//clk, reset
//{{{
initial begin
        CLK = 0;
        forever #10 CLK = ~CLK;
end

initial begin
        RESET = ~TB_RESET_VALUE;
        #100;
            RESET = TB_RESET_VALUE;
        #20;
            RESET = ~TB_RESET_VALUE;
        #10000000;

            $finish;
end    

always @( posedge CLK )
begin
	if (RESET == TB_RESET_VALUE) begin
		CLK_COUNTER <= 0;
	end
	else begin
		CLK_COUNTER <= CLK_COUNTER + 1;
	end
end
//}}}



endmodule
