
//这个东西的作用就是个二路选择器，两个input，看sel来选择输出谁
//区别就在于，
//1. Mux2xOutBits32是一个top型的东西，固定位宽32
//2. commonlib_muxn__N2__width32和Mux2xOutBits32功能其实一模一样，但是是个lab里call出来的
//3. coreir_mux是一个通用的选择器，可以配置位宽的，应该是coreir那个库里生成的




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
