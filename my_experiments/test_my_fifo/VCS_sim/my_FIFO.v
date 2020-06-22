module coreir_reg #(
    parameter width = 1,
    parameter clk_posedge = 1,
    parameter init = 1
) (
    input clk,
    input [width-1:0] in,
    output [width-1:0] out
);
  reg [width-1:0] outReg=init;
  wire real_clk;
  assign real_clk = clk_posedge ? clk : ~clk;
  always @(posedge real_clk) begin
    outReg <= in;
  end
  assign out = outReg;
endmodule

module coreir_mux #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    input sel,
    output [width-1:0] out
);
  assign out = sel ? in1 : in0;
endmodule

module coreir_mem #(
    parameter has_init = 1'b0,
    parameter depth = 1,
    parameter width = 1
) (
    input clk,
    input [width-1:0] wdata,
    input [$clog2(depth)-1:0] waddr,
    input wen,
    output [width-1:0] rdata,
    input [$clog2(depth)-1:0] raddr
);
  reg [width-1:0] data[depth-1:0];
  always @(posedge clk) begin
    if (wen) begin
      data[waddr] <= wdata;
    end
  end
  assign rdata = data[raddr];
endmodule

module coreir_eq #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output out
);
  assign out = in0 == in1;
endmodule

module coreir_const #(
    parameter width = 1,
    parameter value = 1
) (
    output [width-1:0] out
);
  assign out = value;
endmodule

module coreir_add #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output [width-1:0] out
);
  assign out = in0 + in1;
endmodule

module corebit_xor (
    input in0,
    input in1,
    output out
);
  assign out = in0 ^ in1;
endmodule

module corebit_not (
    input in,
    output out
);
  assign out = ~in;
endmodule

module corebit_and (
    input in0,
    input in1,
    output out
);
  assign out = in0 & in1;
endmodule

module commonlib_muxn__N2__width3 (
    input [2:0] in_data_0,
    input [2:0] in_data_1,
    input [0:0] in_sel,
    output [2:0] out
);
wire [2:0] _join_out;
coreir_mux #(
    .width(3)
) _join (
    .in0(in_data_0),
    .in1(in_data_1),
    .sel(in_sel[0]),
    .out(_join_out)
);
assign out = _join_out;
endmodule

module RAM4x32 (
    input [1:0] RADDR,
    output [31:0] RDATA,
    input [1:0] WADDR,
    input [31:0] WDATA,
    input CLK,
    input WE
);
wire [31:0] coreir_mem4x32_inst0_rdata;
coreir_mem #(
    .depth(4),
    .has_init(1'b0),
    .width(32)
) coreir_mem4x32_inst0 (
    .clk(CLK),
    .wdata(WDATA),
    .waddr(WADDR),
    .wen(WE),
    .rdata(coreir_mem4x32_inst0_rdata),
    .raddr(RADDR)
);
assign RDATA = coreir_mem4x32_inst0_rdata;
endmodule

module Mux2xOutBits3 (
    input [2:0] I0,
    input [2:0] I1,
    input S,
    output [2:0] O
);
wire [2:0] coreir_commonlib_mux2x3_inst0_out;
commonlib_muxn__N2__width3 coreir_commonlib_mux2x3_inst0 (
    .in_data_0(I0),
    .in_data_1(I1),
    .in_sel(S),
    .out(coreir_commonlib_mux2x3_inst0_out)
);
assign O = coreir_commonlib_mux2x3_inst0_out;
endmodule

module FIFOGenerator (
    input ARES_design_CLK,
    output ARES_design_Empty,
    output ARES_design_Full,
    output [31:0] ARES_design_RData,
    input ARES_design_RESET,
    input ARES_design_Read,
    input [31:0] ARES_design_WData,
    input ARES_design_Write
);
wire [2:0] Mux2xOutBits3_inst0_O;
wire [2:0] Mux2xOutBits3_inst1_O;
wire [2:0] Mux2xOutBits3_inst2_O;
wire [2:0] Mux2xOutBits3_inst3_O;
wire [31:0] RAM4x32_inst0_RDATA;
wire [2:0] const_0_3_out;
wire [2:0] const_1_3_out;
wire magma_Bit_and_inst0_out;
wire magma_Bit_and_inst1_out;
wire magma_Bit_and_inst2_out;
wire magma_Bit_not_inst0_out;
wire magma_Bit_not_inst1_out;
wire magma_Bit_xor_inst0_out;
wire magma_Bits_2_eq_inst0_out;
wire [2:0] magma_Bits_3_add_inst0_out;
wire [2:0] magma_Bits_3_add_inst1_out;
wire magma_Bits_3_eq_inst0_out;
wire [2:0] reg_P_inst0_out;
wire [2:0] reg_P_inst1_out;
Mux2xOutBits3 Mux2xOutBits3_inst0 (
    .I0(reg_P_inst1_out),
    .I1(magma_Bits_3_add_inst0_out),
    .S(magma_Bit_and_inst1_out),
    .O(Mux2xOutBits3_inst0_O)
);
Mux2xOutBits3 Mux2xOutBits3_inst1 (
    .I0(Mux2xOutBits3_inst0_O),
    .I1(const_0_3_out),
    .S(ARES_design_RESET),
    .O(Mux2xOutBits3_inst1_O)
);
Mux2xOutBits3 Mux2xOutBits3_inst2 (
    .I0(reg_P_inst0_out),
    .I1(magma_Bits_3_add_inst1_out),
    .S(magma_Bit_and_inst2_out),
    .O(Mux2xOutBits3_inst2_O)
);
Mux2xOutBits3 Mux2xOutBits3_inst3 (
    .I0(Mux2xOutBits3_inst2_O),
    .I1(const_0_3_out),
    .S(ARES_design_RESET),
    .O(Mux2xOutBits3_inst3_O)
);
RAM4x32 RAM4x32_inst0 (
    .RADDR({reg_P_inst0_out[1],reg_P_inst0_out[0]}),
    .RDATA(RAM4x32_inst0_RDATA),
    .WADDR({reg_P_inst1_out[1],reg_P_inst1_out[0]}),
    .WDATA(ARES_design_WData),
    .CLK(ARES_design_CLK),
    .WE(magma_Bit_and_inst1_out)
);
coreir_const #(
    .value(3'h0),
    .width(3)
) const_0_3 (
    .out(const_0_3_out)
);
coreir_const #(
    .value(3'h1),
    .width(3)
) const_1_3 (
    .out(const_1_3_out)
);
corebit_and magma_Bit_and_inst0 (
    .in0(magma_Bits_2_eq_inst0_out),
    .in1(magma_Bit_xor_inst0_out),
    .out(magma_Bit_and_inst0_out)
);
corebit_and magma_Bit_and_inst1 (
    .in0(ARES_design_Write),
    .in1(magma_Bit_not_inst0_out),
    .out(magma_Bit_and_inst1_out)
);
corebit_and magma_Bit_and_inst2 (
    .in0(ARES_design_Read),
    .in1(magma_Bit_not_inst1_out),
    .out(magma_Bit_and_inst2_out)
);
corebit_not magma_Bit_not_inst0 (
    .in(magma_Bit_and_inst0_out),
    .out(magma_Bit_not_inst0_out)
);
corebit_not magma_Bit_not_inst1 (
    .in(magma_Bits_3_eq_inst0_out),
    .out(magma_Bit_not_inst1_out)
);
corebit_xor magma_Bit_xor_inst0 (
    .in0(reg_P_inst0_out[2]),
    .in1(reg_P_inst1_out[2]),
    .out(magma_Bit_xor_inst0_out)
);
coreir_eq #(
    .width(2)
) magma_Bits_2_eq_inst0 (
    .in0({reg_P_inst0_out[1],reg_P_inst0_out[0]}),
    .in1({reg_P_inst1_out[1],reg_P_inst1_out[0]}),
    .out(magma_Bits_2_eq_inst0_out)
);
coreir_add #(
    .width(3)
) magma_Bits_3_add_inst0 (
    .in0(reg_P_inst1_out),
    .in1(const_1_3_out),
    .out(magma_Bits_3_add_inst0_out)
);
coreir_add #(
    .width(3)
) magma_Bits_3_add_inst1 (
    .in0(reg_P_inst0_out),
    .in1(const_1_3_out),
    .out(magma_Bits_3_add_inst1_out)
);
coreir_eq #(
    .width(3)
) magma_Bits_3_eq_inst0 (
    .in0(reg_P_inst0_out),
    .in1(reg_P_inst1_out),
    .out(magma_Bits_3_eq_inst0_out)
);
coreir_reg #(
    .clk_posedge(1'b1),
    .init(3'h0),
    .width(3)
) reg_P_inst0 (
    .clk(ARES_design_CLK),
    .in(Mux2xOutBits3_inst3_O),
    .out(reg_P_inst0_out)
);
coreir_reg #(
    .clk_posedge(1'b1),
    .init(3'h0),
    .width(3)
) reg_P_inst1 (
    .clk(ARES_design_CLK),
    .in(Mux2xOutBits3_inst1_O),
    .out(reg_P_inst1_out)
);
assign ARES_design_Empty = magma_Bits_3_eq_inst0_out;
assign ARES_design_Full = magma_Bit_and_inst0_out;
assign ARES_design_RData = RAM4x32_inst0_RDATA;
endmodule

