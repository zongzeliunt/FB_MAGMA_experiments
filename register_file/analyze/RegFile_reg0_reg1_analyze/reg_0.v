
module Register_has_ce_True_has_reset_True_has_async_reset_False_has_async_resetn_False_type_Bits_n_32 (
    input [31:0] I,
    output [31:0] O,
    input CLK,
    input CE,
    input RESET
);
wire [31:0] Mux2xOutBits32_inst0_O;
wire [31:0] const_1_32_out;
wire [31:0] enable_mux_O;
wire [31:0] value_out;


//Mux2xOutBits32_inst0_O被输出给coreir_reg
//在reset的时候给写1，其他时候写enable_mux_O
Mux2xOutBits32 Mux2xOutBits32_inst0 (
    .I0(enable_mux_O),
    .I1(const_1_32_out),
    .S(RESET),
    .O(Mux2xOutBits32_inst0_O)
);

//coreir_const固定输出32位宽数1,
coreir_const #(
    .value('h00000001),
    .width(32)
) const_1_32 (
    .out(const_1_32_out)
);

//enable_mux这里有点像自刷新，一直是用value_out给enable_mux_O刷新，除了CE为高的时候才把I刷入
Mux2xOutBits32 enable_mux (
    .I0(value_out),
    .I1(I),
    .S(CE),
    .O(enable_mux_O)
);


//coreir_reg很简单，每个clk把in写进去，把outReg写到out
coreir_reg #(
    .clk_posedge(1'b1),
    .init('h00000001),
    .width(32)
) value (
    .clk(CLK),
    .in(Mux2xOutBits32_inst0_O),
    .out(value_out)
);
assign O = value_out;







endmodule

