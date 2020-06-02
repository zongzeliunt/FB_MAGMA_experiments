module RegFile_reg0_reg1 (
    input [0:0] apb_PADDR,
    input apb_PCLK,
    input apb_PENABLE,
    input apb_PPROT,
    output [31:0] apb_PRDATA,
    output apb_PREADY,
    input apb_PRESETn,
    input apb_PSEL1,
    output apb_PSLVERR,
    input [3:0] apb_PSTRB,
    input [31:0] apb_PWDATA,
    input apb_PWRITE,



    input [31:0] reg0_d,
    input reg0_en,
    output [31:0] reg0_q,
    input [31:0] reg1_d,
    output [31:0] reg1_q
);
wire [31:0] Mux2xOutBits32_inst0_O;
wire [31:0] Mux2xOutBits32_inst1_O;
wire [31:0] Mux2xOutBits32_inst2_O;
wire [0:0] const_0_1_out;
wire [0:0] const_1_1_out;
wire corebit_undriven_inst0_out;
wire magma_Bit_and_inst0_out;
//magma_Bit_and_inst1_out就是写使能，
//design是is_write = io.apb.PENABLE & io.apb.PWRITE & PSEL
wire magma_Bit_and_inst1_out;


wire magma_Bit_and_inst2_out;
wire magma_Bit_and_inst3_out;
wire magma_Bit_and_inst4_out;
wire magma_Bit_and_inst5_out;
wire magma_Bit_not_inst0_out;
wire magma_Bit_not_inst1_out;
wire magma_Bit_not_inst2_out;
wire magma_Bit_or_inst0_out;
wire magma_Bit_or_inst1_out;
wire magma_Bit_or_inst2_out;
wire magma_Bits_1_eq_inst0_out;
wire magma_Bits_1_eq_inst1_out;
wire [31:0] reg0_O;
wire [31:0] reg1_O;
corebit_not magma_Bit_not_inst0 (
    .in(apb_PRESETn),
    .out(magma_Bit_not_inst0_out)
);

//reset
//{{{
corebit_not magma_Bit_not_inst1 (
    .in(apb_PRESETn),
    .out(magma_Bit_not_inst1_out)
);
//}}}

assign apb_PRDATA = Mux2xOutBits32_inst2_O;
assign apb_PREADY = magma_Bit_or_inst2_out;
assign apb_PSLVERR = corebit_undriven_inst0_out;
assign reg0_q = reg0_O;
assign reg1_q = reg1_O;


//is_write = io.apb.PENABLE & io.apb.PWRITE & PSEL
//{{{
corebit_and magma_Bit_and_inst0 (
    .in0(apb_PENABLE),
    .in1(apb_PWRITE),
    .out(magma_Bit_and_inst0_out)
);

corebit_and magma_Bit_and_inst1 (
    .in0(magma_Bit_and_inst0_out),
    .in1(apb_PSEL1),
    .out(magma_Bit_and_inst1_out)
);
//}}}


//is_read = io.apb.PENABLE & ~io.apb.PWRITE & PSEL
//{{{
//~io.apb.PWRITE
corebit_not magma_Bit_not_inst2 (
    .in(apb_PWRITE),
    .out(magma_Bit_not_inst2_out)
);

corebit_and magma_Bit_and_inst4 (
    .in0(apb_PENABLE),
    .in1(magma_Bit_not_inst2_out),
    .out(magma_Bit_and_inst4_out)
);

corebit_and magma_Bit_and_inst5 (
    .in0(magma_Bit_and_inst4_out),
    .in1(apb_PSEL1),
    .out(magma_Bit_and_inst5_out)
);
//}}}

//reg_0
//{{{


//write data
Mux2xOutBits32 Mux2xOutBits32_inst0 (
    .I0(reg0_d),
    .I1(apb_PWDATA),
    .S(magma_Bit_and_inst1_out),
    .O(Mux2xOutBits32_inst0_O)
);

//write 信号
//magma_Bit_and_inst1_out是写使能
//magma_Bits_1_eq_inst0_out是地址到了reg_1那一位了
//magma_Bit_and_inst2_out就是reg_0的可write信号，加上CE的判断就能连上reg_0的CE了
"""
            ce = is_write & (io.apb.PADDR == i)
            if regs[i].has_ce:
                reg.CE @= ce | m.bit(getattr(io, reg.name + "_en"))
            else:
                reg.CE @= ce
"""

coreir_const #(
    .value(1'h0),
    .width(1)
) const_0_1 (
    .out(const_0_1_out)
);

coreir_eq #(
    .width(1)
) magma_Bits_1_eq_inst0 (
    .in0(apb_PADDR),
    .in1(const_0_1_out),
    .out(magma_Bits_1_eq_inst0_out)
);
//magma_Bit_and_inst1_out就是is_write
//magma_Bits_1_eq_inst0_out就是io.apb.PADDR == i
//magma_Bit_and_inst2_out就是ce
corebit_and magma_Bit_and_inst2 (
    .in0(magma_Bit_and_inst1_out),
    .in1(magma_Bits_1_eq_inst0_out),
    .out(magma_Bit_and_inst2_out)
);

//CE
//reg.CE @= ce | m.bit(getattr(io, reg.name + "_en"))
corebit_or magma_Bit_or_inst0 (
    .in0(magma_Bit_and_inst2_out),
    .in1(reg0_en),
    .out(magma_Bit_or_inst0_out)
);

Register_has_ce_True_has_reset_True_has_async_reset_False_has_async_resetn_False_type_Bits_n_32 reg0 (
    .I(Mux2xOutBits32_inst0_O),
    .O(reg0_O),
    .CLK(apb_PCLK),
    .CE(magma_Bit_or_inst0_out),
    .RESET(magma_Bit_not_inst0_out)
);
//}}}


//reg_1
//{{{
//write data
Mux2xOutBits32 Mux2xOutBits32_inst1 (
    .I0(reg1_d),
    .I1(apb_PWDATA),
    .S(magma_Bit_and_inst1_out),
    .O(Mux2xOutBits32_inst1_O)
);

//write 信号
//magma_Bit_and_inst1_out是写使能
//magma_Bits_1_eq_inst1_out是地址到了reg_1那一位了
//magma_Bit_and_inst3_out直接连上reg_1的CE信号
"""
            ce = is_write & (io.apb.PADDR == i)
            if regs[i].has_ce:
                reg.CE @= ce | m.bit(getattr(io, reg.name + "_en"))
            else:
                reg.CE @= ce
"""

coreir_const #(
    .value(1'h1),
    .width(1)
) const_1_1 (
    .out(const_1_1_out)
);

coreir_eq #(
    .width(1)
) magma_Bits_1_eq_inst1 (
    .in0(apb_PADDR),
    .in1(const_1_1_out),
    .out(magma_Bits_1_eq_inst1_out)
);

//magma_Bit_and_inst1_out就是is_write
//magma_Bits_1_eq_inst1_out就是io.apb.PADDR == i
//magma_Bit_and_inst3_out就是ce

//CE, reg_1有CE，但是top没有reg_1的CE，只是生成一个信号敷衍一下
//reg.CE @= ce
corebit_and magma_Bit_and_inst3 (
    .in0(magma_Bit_and_inst1_out),
    .in1(magma_Bits_1_eq_inst1_out),
    .out(magma_Bit_and_inst3_out)
);


Register_has_ce_True_has_reset_True_has_async_reset_False_has_async_resetn_False_type_Bits_n_32_unq1 reg1 (
    .I(Mux2xOutBits32_inst1_O),
    .O(reg1_O),
    .CLK(apb_PCLK),
    .CE(magma_Bit_and_inst3_out),
    .RESET(magma_Bit_not_inst1_out)
);



//}}}


//read 操作和PREADY信号
//{{{
//magma_Bit_and_inst2_out 代表reg_0写完，就是ready
//magma_Bit_and_inst3_out 代表reg_1写完，就是ready
//magma_Bit_and_inst5_out 就是resign里的is_read信号
//ready信号
"""
if ready is not None:
    ready |= ce
else:
    ready = ce
"""
corebit_or magma_Bit_or_inst1 (
    .in0(magma_Bit_and_inst2_out),
    .in1(magma_Bit_and_inst3_out),
    .out(magma_Bit_or_inst1_out)
);


//io.apb.PREADY @= ready | is_read
//RTL里有：assign apb_PREADY = magma_Bit_or_inst2_out;
corebit_or magma_Bit_or_inst2 (
    .in0(magma_Bit_or_inst1_out),
    .in1(magma_Bit_and_inst5_out),
    .out(magma_Bit_or_inst2_out)
);
//}}}


//总读
//用apb_PADDR来管输出哪个
//io.apb.PRDATA @= mantle.mux([reg.O for reg in registers], io.apb.PADDR)
//{{{
Mux2xOutBits32 Mux2xOutBits32_inst2 (
    .I0(reg0_O),
    .I1(reg1_O),
    .S(apb_PADDR[0]),
    .O(Mux2xOutBits32_inst2_O)
);
//}}}

//useless
//{{{
//io.apb.PSTRB.unused()
coreir_term #(
    .width(4)
) term_inst0 (
    .in(apb_PSTRB)
);

//io.apb.PPROT.unused()
corebit_term corebit_term_inst0 (
    .in(apb_PPROT)
);

//RTL: assign apb_PSLVERR = corebit_undriven_inst0_out;
corebit_undriven corebit_undriven_inst0 (
    .out(corebit_undriven_inst0_out)
);
//}}}

endmodule

