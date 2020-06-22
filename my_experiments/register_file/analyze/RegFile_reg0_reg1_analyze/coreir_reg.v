
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





//useless
//{{{

module coreir_term #(
    parameter width = 1
) (
    input [width-1:0] in
);

endmodule


module corebit_undriven (
    output out
);

endmodule

module corebit_term (
    input in
);

endmodule
//}}}

