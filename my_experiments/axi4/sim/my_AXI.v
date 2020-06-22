module coreir_sub #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output [width-1:0] out
);
  assign out = in0 - in1;
endmodule

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

module corebit_not (
    input in,
    output out
);
  assign out = ~in;
endmodule

module corebit_const #(
    parameter value = 1
) (
    output out
);
  assign out = value;
endmodule

module corebit_and (
    input in0,
    input in1,
    output out
);
  assign out = in0 & in1;
endmodule

module commonlib_muxn__N2__width32 (
    input [31:0] in_data_0,
    input [31:0] in_data_1,
    input [0:0] in_sel,
    output [31:0] out
);
wire [31:0] _join_out;
coreir_mux #(
    .width(32)
) _join (
    .in0(in_data_0),
    .in1(in_data_1),
    .sel(in_sel[0]),
    .out(_join_out)
);
assign out = _join_out;
endmodule

module commonlib_muxn__N2__width1 (
    input [0:0] in_data_0,
    input [0:0] in_data_1,
    input [0:0] in_sel,
    output [0:0] out
);
wire [0:0] _join_out;
coreir_mux #(
    .width(1)
) _join (
    .in0(in_data_0),
    .in1(in_data_1),
    .sel(in_sel[0]),
    .out(_join_out)
);
assign out = _join_out;
endmodule

module RAM32x32 (
    input [4:0] RADDR,
    output [31:0] RDATA,
    input [4:0] WADDR,
    input [31:0] WDATA,
    input CLK,
    input WE
);
wire [31:0] coreir_mem32x32_inst0_rdata;
coreir_mem #(
    .depth(32),
    .has_init(1'b0),
    .width(32)
) coreir_mem32x32_inst0 (
    .clk(CLK),
    .wdata(WDATA),
    .waddr(WADDR),
    .wen(WE),
    .rdata(coreir_mem32x32_inst0_rdata),
    .raddr(RADDR)
);
assign RDATA = coreir_mem32x32_inst0_rdata;
endmodule

module Mux2xOutUInt32 (
    input [31:0] I0,
    input [31:0] I1,
    input S,
    output [31:0] O
);
wire [31:0] coreir_commonlib_mux2x32_inst0_out;
commonlib_muxn__N2__width32 coreir_commonlib_mux2x32_inst0 (
    .in_data_0(I0),
    .in_data_1(I1),
    .in_sel(S),
    .out(coreir_commonlib_mux2x32_inst0_out)
);
assign O = coreir_commonlib_mux2x32_inst0_out;
endmodule

module Mux2xOutBits32 (
    input [31:0] I0,
    input [31:0] I1,
    input S,
    output [31:0] O
);
wire [31:0] coreir_commonlib_mux2x32_inst0_out;
commonlib_muxn__N2__width32 coreir_commonlib_mux2x32_inst0 (
    .in_data_0(I0),
    .in_data_1(I1),
    .in_sel(S),
    .out(coreir_commonlib_mux2x32_inst0_out)
);
assign O = coreir_commonlib_mux2x32_inst0_out;
endmodule

module Mux2xOutBit (
    input I0,
    input I1,
    input S,
    output O
);
wire [0:0] coreir_commonlib_mux2x1_inst0_out;
commonlib_muxn__N2__width1 coreir_commonlib_mux2x1_inst0 (
    .in_data_0(I0),
    .in_data_1(I1),
    .in_sel(S),
    .out(coreir_commonlib_mux2x1_inst0_out)
);
assign O = coreir_commonlib_mux2x1_inst0_out[0];
endmodule

module AXI (
    input ARES_design_CLK,
    input ARES_design_RESET,
    input [31:0] ARES_design_RReq_addr,
    output ARES_design_RReq_ready,
    input [31:0] ARES_design_RReq_size,
    input ARES_design_RReq_valid,
    output [31:0] ARES_design_R_data,
    input ARES_design_R_ready,
    output ARES_design_R_valid,
    input [31:0] ARES_design_WReq_addr,
    output ARES_design_WReq_ready,
    input [31:0] ARES_design_WReq_size,
    input ARES_design_WReq_valid,
    input [31:0] ARES_design_W_data,
    output ARES_design_W_ready,
    input ARES_design_W_valid
);
wire Mux2xOutBit_inst0_O;
wire Mux2xOutBit_inst1_O;
wire Mux2xOutBit_inst2_O;
wire Mux2xOutBit_inst3_O;
wire [31:0] Mux2xOutBits32_inst0_O;
wire [31:0] Mux2xOutBits32_inst1_O;
wire [31:0] Mux2xOutBits32_inst2_O;
wire [31:0] Mux2xOutBits32_inst3_O;
wire [31:0] Mux2xOutUInt32_inst0_O;
wire [31:0] Mux2xOutUInt32_inst1_O;
wire [31:0] Mux2xOutUInt32_inst10_O;
wire [31:0] Mux2xOutUInt32_inst11_O;
wire [31:0] Mux2xOutUInt32_inst12_O;
wire [31:0] Mux2xOutUInt32_inst13_O;
wire [31:0] Mux2xOutUInt32_inst14_O;
wire [31:0] Mux2xOutUInt32_inst15_O;
wire [31:0] Mux2xOutUInt32_inst2_O;
wire [31:0] Mux2xOutUInt32_inst3_O;
wire [31:0] Mux2xOutUInt32_inst4_O;
wire [31:0] Mux2xOutUInt32_inst5_O;
wire [31:0] Mux2xOutUInt32_inst6_O;
wire [31:0] Mux2xOutUInt32_inst7_O;
wire [31:0] Mux2xOutUInt32_inst8_O;
wire [31:0] Mux2xOutUInt32_inst9_O;
wire [31:0] RAM32x32_inst0_RDATA;
wire bit_const_0_None_out;
wire bit_const_1_None_out;
wire [31:0] const_0_32_out;
wire [31:0] const_1_32_out;
wire [4:0] coreir_add5_inst0_out;
wire [4:0] coreir_add5_inst1_out;
wire magma_Bit_and_inst0_out;
wire magma_Bit_and_inst1_out;
wire magma_Bit_and_inst2_out;
wire magma_Bit_and_inst3_out;
wire magma_Bit_not_inst0_out;
wire magma_Bit_not_inst1_out;
wire magma_Bit_not_inst2_out;
wire magma_Bit_not_inst3_out;
wire magma_Bit_not_inst4_out;
wire magma_Bit_not_inst5_out;
wire [31:0] magma_Bits_32_add_inst0_out;
wire [31:0] magma_Bits_32_add_inst1_out;
wire magma_Bits_32_eq_inst0_out;
wire magma_Bits_32_eq_inst1_out;
wire [31:0] magma_Bits_32_sub_inst0_out;
wire [31:0] magma_Bits_32_sub_inst1_out;
wire [31:0] reg_P_inst0_out;
wire [31:0] reg_P_inst1_out;
wire [31:0] reg_P_inst2_out;
wire [31:0] reg_P_inst3_out;
wire [31:0] reg_P_inst4_out;
wire [31:0] reg_P_inst5_out;
Mux2xOutBit Mux2xOutBit_inst0 (
    .I0(magma_Bit_not_inst1_out),
    .I1(bit_const_1_None_out),
    .S(ARES_design_RESET),
    .O(Mux2xOutBit_inst0_O)
);
Mux2xOutBit Mux2xOutBit_inst1 (
    .I0(magma_Bit_not_inst0_out),
    .I1(bit_const_0_None_out),
    .S(ARES_design_RESET),
    .O(Mux2xOutBit_inst1_O)
);
Mux2xOutBit Mux2xOutBit_inst2 (
    .I0(magma_Bit_not_inst4_out),
    .I1(bit_const_1_None_out),
    .S(ARES_design_RESET),
    .O(Mux2xOutBit_inst2_O)
);
Mux2xOutBit Mux2xOutBit_inst3 (
    .I0(magma_Bit_not_inst3_out),
    .I1(bit_const_0_None_out),
    .S(ARES_design_RESET),
    .O(Mux2xOutBit_inst3_O)
);
Mux2xOutBits32 Mux2xOutBits32_inst0 (
    .I0(reg_P_inst0_out),
    .I1(magma_Bits_32_sub_inst0_out),
    .S(magma_Bit_and_inst1_out),
    .O(Mux2xOutBits32_inst0_O)
);
Mux2xOutBits32 Mux2xOutBits32_inst1 (
    .I0(reg_P_inst2_out),
    .I1(magma_Bits_32_add_inst0_out),
    .S(magma_Bit_and_inst1_out),
    .O(Mux2xOutBits32_inst1_O)
);
Mux2xOutBits32 Mux2xOutBits32_inst2 (
    .I0(reg_P_inst3_out),
    .I1(magma_Bits_32_sub_inst1_out),
    .S(magma_Bit_and_inst3_out),
    .O(Mux2xOutBits32_inst2_O)
);
Mux2xOutBits32 Mux2xOutBits32_inst3 (
    .I0(reg_P_inst5_out),
    .I1(magma_Bits_32_add_inst1_out),
    .S(magma_Bit_and_inst3_out),
    .O(Mux2xOutBits32_inst3_O)
);
Mux2xOutUInt32 Mux2xOutUInt32_inst0 (
    .I0(const_0_32_out),
    .I1(ARES_design_WReq_size),
    .S(magma_Bit_and_inst0_out),
    .O(Mux2xOutUInt32_inst0_O)
);
Mux2xOutUInt32 Mux2xOutUInt32_inst1 (
    .I0(const_0_32_out),
    .I1(ARES_design_WReq_addr),
    .S(magma_Bit_and_inst0_out),
    .O(Mux2xOutUInt32_inst1_O)
);
Mux2xOutUInt32 Mux2xOutUInt32_inst10 (
    .I0(Mux2xOutUInt32_inst8_O),
    .I1(Mux2xOutBits32_inst2_O),
    .S(magma_Bit_not_inst3_out),
    .O(Mux2xOutUInt32_inst10_O)
);
Mux2xOutUInt32 Mux2xOutUInt32_inst11 (
    .I0(Mux2xOutUInt32_inst10_O),
    .I1(const_0_32_out),
    .S(ARES_design_RESET),
    .O(Mux2xOutUInt32_inst11_O)
);
Mux2xOutUInt32 Mux2xOutUInt32_inst12 (
    .I0(Mux2xOutUInt32_inst9_O),
    .I1(reg_P_inst4_out),
    .S(magma_Bit_not_inst3_out),
    .O(Mux2xOutUInt32_inst12_O)
);
Mux2xOutUInt32 Mux2xOutUInt32_inst13 (
    .I0(Mux2xOutUInt32_inst12_O),
    .I1(const_0_32_out),
    .S(ARES_design_RESET),
    .O(Mux2xOutUInt32_inst13_O)
);
Mux2xOutUInt32 Mux2xOutUInt32_inst14 (
    .I0(const_0_32_out),
    .I1(Mux2xOutBits32_inst3_O),
    .S(magma_Bit_not_inst3_out),
    .O(Mux2xOutUInt32_inst14_O)
);
Mux2xOutUInt32 Mux2xOutUInt32_inst15 (
    .I0(Mux2xOutUInt32_inst14_O),
    .I1(const_0_32_out),
    .S(ARES_design_RESET),
    .O(Mux2xOutUInt32_inst15_O)
);
Mux2xOutUInt32 Mux2xOutUInt32_inst2 (
    .I0(Mux2xOutUInt32_inst0_O),
    .I1(Mux2xOutBits32_inst0_O),
    .S(magma_Bit_not_inst0_out),
    .O(Mux2xOutUInt32_inst2_O)
);
Mux2xOutUInt32 Mux2xOutUInt32_inst3 (
    .I0(Mux2xOutUInt32_inst2_O),
    .I1(const_0_32_out),
    .S(ARES_design_RESET),
    .O(Mux2xOutUInt32_inst3_O)
);
Mux2xOutUInt32 Mux2xOutUInt32_inst4 (
    .I0(Mux2xOutUInt32_inst1_O),
    .I1(reg_P_inst1_out),
    .S(magma_Bit_not_inst0_out),
    .O(Mux2xOutUInt32_inst4_O)
);
Mux2xOutUInt32 Mux2xOutUInt32_inst5 (
    .I0(Mux2xOutUInt32_inst4_O),
    .I1(const_0_32_out),
    .S(ARES_design_RESET),
    .O(Mux2xOutUInt32_inst5_O)
);
Mux2xOutUInt32 Mux2xOutUInt32_inst6 (
    .I0(const_0_32_out),
    .I1(Mux2xOutBits32_inst1_O),
    .S(magma_Bit_not_inst0_out),
    .O(Mux2xOutUInt32_inst6_O)
);
Mux2xOutUInt32 Mux2xOutUInt32_inst7 (
    .I0(Mux2xOutUInt32_inst6_O),
    .I1(const_0_32_out),
    .S(ARES_design_RESET),
    .O(Mux2xOutUInt32_inst7_O)
);
Mux2xOutUInt32 Mux2xOutUInt32_inst8 (
    .I0(const_0_32_out),
    .I1(ARES_design_RReq_size),
    .S(magma_Bit_and_inst2_out),
    .O(Mux2xOutUInt32_inst8_O)
);
Mux2xOutUInt32 Mux2xOutUInt32_inst9 (
    .I0(const_0_32_out),
    .I1(ARES_design_RReq_addr),
    .S(magma_Bit_and_inst2_out),
    .O(Mux2xOutUInt32_inst9_O)
);
RAM32x32 RAM32x32_inst0 (
    .RADDR(coreir_add5_inst1_out),
    .RDATA(RAM32x32_inst0_RDATA),
    .WADDR(coreir_add5_inst0_out),
    .WDATA(ARES_design_W_data),
    .CLK(ARES_design_CLK),
    .WE(magma_Bit_and_inst1_out)
);
corebit_const #(
    .value(1'b0)
) bit_const_0_None (
    .out(bit_const_0_None_out)
);
corebit_const #(
    .value(1'b1)
) bit_const_1_None (
    .out(bit_const_1_None_out)
);
coreir_const #(
    .value('h00000000),
    .width(32)
) const_0_32 (
    .out(const_0_32_out)
);
coreir_const #(
    .value('h00000001),
    .width(32)
) const_1_32 (
    .out(const_1_32_out)
);
coreir_add #(
    .width(5)
) coreir_add5_inst0 (
    .in0({reg_P_inst1_out[4],reg_P_inst1_out[3],reg_P_inst1_out[2],reg_P_inst1_out[1],reg_P_inst1_out[0]}),
    .in1({reg_P_inst2_out[4],reg_P_inst2_out[3],reg_P_inst2_out[2],reg_P_inst2_out[1],reg_P_inst2_out[0]}),
    .out(coreir_add5_inst0_out)
);
coreir_add #(
    .width(5)
) coreir_add5_inst1 (
    .in0({reg_P_inst4_out[4],reg_P_inst4_out[3],reg_P_inst4_out[2],reg_P_inst4_out[1],reg_P_inst4_out[0]}),
    .in1({reg_P_inst5_out[4],reg_P_inst5_out[3],reg_P_inst5_out[2],reg_P_inst5_out[1],reg_P_inst5_out[0]}),
    .out(coreir_add5_inst1_out)
);
corebit_and magma_Bit_and_inst0 (
    .in0(ARES_design_WReq_valid),
    .in1(magma_Bit_not_inst2_out),
    .out(magma_Bit_and_inst0_out)
);
corebit_and magma_Bit_and_inst1 (
    .in0(ARES_design_W_valid),
    .in1(magma_Bit_not_inst0_out),
    .out(magma_Bit_and_inst1_out)
);
corebit_and magma_Bit_and_inst2 (
    .in0(ARES_design_RReq_valid),
    .in1(magma_Bit_not_inst5_out),
    .out(magma_Bit_and_inst2_out)
);
corebit_and magma_Bit_and_inst3 (
    .in0(ARES_design_R_ready),
    .in1(magma_Bit_not_inst3_out),
    .out(magma_Bit_and_inst3_out)
);
corebit_not magma_Bit_not_inst0 (
    .in(magma_Bits_32_eq_inst0_out),
    .out(magma_Bit_not_inst0_out)
);
corebit_not magma_Bit_not_inst1 (
    .in(magma_Bit_not_inst0_out),
    .out(magma_Bit_not_inst1_out)
);
corebit_not magma_Bit_not_inst2 (
    .in(magma_Bit_not_inst0_out),
    .out(magma_Bit_not_inst2_out)
);
corebit_not magma_Bit_not_inst3 (
    .in(magma_Bits_32_eq_inst1_out),
    .out(magma_Bit_not_inst3_out)
);
corebit_not magma_Bit_not_inst4 (
    .in(magma_Bit_not_inst3_out),
    .out(magma_Bit_not_inst4_out)
);
corebit_not magma_Bit_not_inst5 (
    .in(magma_Bit_not_inst3_out),
    .out(magma_Bit_not_inst5_out)
);
coreir_add #(
    .width(32)
) magma_Bits_32_add_inst0 (
    .in0(reg_P_inst2_out),
    .in1(const_1_32_out),
    .out(magma_Bits_32_add_inst0_out)
);
coreir_add #(
    .width(32)
) magma_Bits_32_add_inst1 (
    .in0(reg_P_inst5_out),
    .in1(const_1_32_out),
    .out(magma_Bits_32_add_inst1_out)
);
coreir_eq #(
    .width(32)
) magma_Bits_32_eq_inst0 (
    .in0(reg_P_inst0_out),
    .in1(const_0_32_out),
    .out(magma_Bits_32_eq_inst0_out)
);
coreir_eq #(
    .width(32)
) magma_Bits_32_eq_inst1 (
    .in0(reg_P_inst3_out),
    .in1(const_0_32_out),
    .out(magma_Bits_32_eq_inst1_out)
);
coreir_sub #(
    .width(32)
) magma_Bits_32_sub_inst0 (
    .in0(reg_P_inst0_out),
    .in1(const_1_32_out),
    .out(magma_Bits_32_sub_inst0_out)
);
coreir_sub #(
    .width(32)
) magma_Bits_32_sub_inst1 (
    .in0(reg_P_inst3_out),
    .in1(const_1_32_out),
    .out(magma_Bits_32_sub_inst1_out)
);
coreir_reg #(
    .clk_posedge(1'b1),
    .init('h00000000),
    .width(32)
) reg_P_inst0 (
    .clk(ARES_design_CLK),
    .in(Mux2xOutUInt32_inst3_O),
    .out(reg_P_inst0_out)
);
coreir_reg #(
    .clk_posedge(1'b1),
    .init('h00000000),
    .width(32)
) reg_P_inst1 (
    .clk(ARES_design_CLK),
    .in(Mux2xOutUInt32_inst5_O),
    .out(reg_P_inst1_out)
);
coreir_reg #(
    .clk_posedge(1'b1),
    .init('h00000000),
    .width(32)
) reg_P_inst2 (
    .clk(ARES_design_CLK),
    .in(Mux2xOutUInt32_inst7_O),
    .out(reg_P_inst2_out)
);
coreir_reg #(
    .clk_posedge(1'b1),
    .init('h00000000),
    .width(32)
) reg_P_inst3 (
    .clk(ARES_design_CLK),
    .in(Mux2xOutUInt32_inst11_O),
    .out(reg_P_inst3_out)
);
coreir_reg #(
    .clk_posedge(1'b1),
    .init('h00000000),
    .width(32)
) reg_P_inst4 (
    .clk(ARES_design_CLK),
    .in(Mux2xOutUInt32_inst13_O),
    .out(reg_P_inst4_out)
);
coreir_reg #(
    .clk_posedge(1'b1),
    .init('h00000000),
    .width(32)
) reg_P_inst5 (
    .clk(ARES_design_CLK),
    .in(Mux2xOutUInt32_inst15_O),
    .out(reg_P_inst5_out)
);
assign ARES_design_RReq_ready = Mux2xOutBit_inst2_O;
assign ARES_design_R_data = RAM32x32_inst0_RDATA;
assign ARES_design_R_valid = Mux2xOutBit_inst3_O;
assign ARES_design_WReq_ready = Mux2xOutBit_inst0_O;
assign ARES_design_W_ready = Mux2xOutBit_inst1_O;
endmodule

