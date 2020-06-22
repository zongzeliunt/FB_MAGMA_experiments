//功能和reg_0差不多，区别就是reset的值是18（24）
//这个24是design里写的，本来design里没写reg_1有CE，但是这里也生成了
module Register_has_ce_True_has_reset_True_has_async_reset_False_has_async_resetn_False_type_Bits_n_32_unq1 (
    input [31:0] I,
    output [31:0] O,
    input CLK,
    input CE,
    input RESET
);
wire [31:0] Mux2xOutBits32_inst0_O;
wire [31:0] const_24_32_out;
wire [31:0] enable_mux_O;
wire [31:0] value_out;
Mux2xOutBits32 Mux2xOutBits32_inst0 (
    .I0(enable_mux_O),
    .I1(const_24_32_out),
    .S(RESET),
    .O(Mux2xOutBits32_inst0_O)
);
coreir_const #(
    .value('h00000018),
    .width(32)
) const_24_32 (
    .out(const_24_32_out)
);
Mux2xOutBits32 enable_mux (
    .I0(value_out),
    .I1(I),
    .S(CE),
    .O(enable_mux_O)
);
coreir_reg #(
    .clk_posedge(1'b1),
    .init('h00000018),
    .width(32)
) value (
    .clk(CLK),
    .in(Mux2xOutBits32_inst0_O),
    .out(value_out)
);
assign O = value_out;
endmodule

