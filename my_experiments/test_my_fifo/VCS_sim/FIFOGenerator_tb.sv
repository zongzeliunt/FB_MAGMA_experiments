`timescale 1ns/1ns
module FIFOGenerator_tb;
    reg ARES_design_CLK;
    reg ARES_design_RESET;
    reg [31:0] ARES_design_WData;
    wire ARES_design_Full;
    reg ARES_design_Write;
    wire [31:0] ARES_design_RData;
    wire ARES_design_Empty;
    reg ARES_design_Read;

    

    FIFOGenerator #(
        
    ) dut (
        .ARES_design_CLK(ARES_design_CLK),
        .ARES_design_RESET(ARES_design_RESET),
        .ARES_design_WData(ARES_design_WData),
        .ARES_design_Full(ARES_design_Full),
        .ARES_design_Write(ARES_design_Write),
        .ARES_design_RData(ARES_design_RData),
        .ARES_design_Empty(ARES_design_Empty),
        .ARES_design_Read(ARES_design_Read)
    );

    initial begin
        $vcdplusfile("waveforms.vpd");
        $vcdpluson();
        $vcdplusmemon();
        ARES_design_CLK <= 1'b0;
        ARES_design_RESET <= 1'b1;
        ARES_design_Write <= 1'b0;
        ARES_design_Read <= 1'b0;
        ARES_design_WData <= 32'd0;
        #5 ARES_design_CLK ^= 1;
        #5 ARES_design_CLK ^= 1;
        ARES_design_RESET <= 1'b0;
        #5 ARES_design_CLK ^= 1;
        #5 ARES_design_CLK ^= 1;
        if (!(ARES_design_Empty === 1'b1)) begin
            $error("Failed on action=8 checking port FIFOGenerator.ARES_design.Empty with traceback /usr/local/lib/python3.7/dist-packages/fault/wrapper.py:62.  Expected %x, got %x.", 1'b1, ARES_design_Empty);
        end
        if (!(ARES_design_Full === 1'b0)) begin
            $error("Failed on action=9 checking port FIFOGenerator.ARES_design.Full with traceback /usr/local/lib/python3.7/dist-packages/fault/wrapper.py:62.  Expected %x, got %x.", 1'b0, ARES_design_Full);
        end
        ARES_design_Write <= 1'b1;
        ARES_design_WData <= 32'd15;
        #5 ARES_design_CLK ^= 1;
        #5 ARES_design_CLK ^= 1;
        if (!(ARES_design_Empty === 1'b0)) begin
            $error("Failed on action=13 checking port FIFOGenerator.ARES_design.Empty with traceback /usr/local/lib/python3.7/dist-packages/fault/wrapper.py:62.  Expected %x, got %x.", 1'b0, ARES_design_Empty);
        end
        if (!(ARES_design_Full === 1'b0)) begin
            $error("Failed on action=14 checking port FIFOGenerator.ARES_design.Full with traceback /usr/local/lib/python3.7/dist-packages/fault/wrapper.py:62.  Expected %x, got %x.", 1'b0, ARES_design_Full);
        end
        ARES_design_Write <= 1'b1;
        ARES_design_WData <= 32'd16;
        #5 ARES_design_CLK ^= 1;
        #5 ARES_design_CLK ^= 1;
        if (!(ARES_design_Empty === 1'b0)) begin
            $error("Failed on action=18 checking port FIFOGenerator.ARES_design.Empty with traceback /usr/local/lib/python3.7/dist-packages/fault/wrapper.py:62.  Expected %x, got %x.", 1'b0, ARES_design_Empty);
        end
        if (!(ARES_design_Full === 1'b0)) begin
            $error("Failed on action=19 checking port FIFOGenerator.ARES_design.Full with traceback /usr/local/lib/python3.7/dist-packages/fault/wrapper.py:62.  Expected %x, got %x.", 1'b0, ARES_design_Full);
        end
        ARES_design_Write <= 1'b1;
        ARES_design_WData <= 32'd17;
        #5 ARES_design_CLK ^= 1;
        #5 ARES_design_CLK ^= 1;
        if (!(ARES_design_Empty === 1'b0)) begin
            $error("Failed on action=23 checking port FIFOGenerator.ARES_design.Empty with traceback /usr/local/lib/python3.7/dist-packages/fault/wrapper.py:62.  Expected %x, got %x.", 1'b0, ARES_design_Empty);
        end
        if (!(ARES_design_Full === 1'b0)) begin
            $error("Failed on action=24 checking port FIFOGenerator.ARES_design.Full with traceback /usr/local/lib/python3.7/dist-packages/fault/wrapper.py:62.  Expected %x, got %x.", 1'b0, ARES_design_Full);
        end
        ARES_design_Write <= 1'b1;
        ARES_design_WData <= 32'd18;
        #5 ARES_design_CLK ^= 1;
        #5 ARES_design_CLK ^= 1;
        if (!(ARES_design_Empty === 1'b0)) begin
            $error("Failed on action=28 checking port FIFOGenerator.ARES_design.Empty with traceback /usr/local/lib/python3.7/dist-packages/fault/wrapper.py:62.  Expected %x, got %x.", 1'b0, ARES_design_Empty);
        end
        if (!(ARES_design_Full === 1'b1)) begin
            $error("Failed on action=29 checking port FIFOGenerator.ARES_design.Full with traceback /usr/local/lib/python3.7/dist-packages/fault/wrapper.py:62.  Expected %x, got %x.", 1'b1, ARES_design_Full);
        end
        ARES_design_Write <= 1'b0;
        if (!(ARES_design_RData === 32'd15)) begin
            $error("Failed on action=31 checking port FIFOGenerator.ARES_design.RData with traceback /usr/local/lib/python3.7/dist-packages/fault/wrapper.py:62.  Expected %x, got %x.", 32'd15, ARES_design_RData);
        end
        ARES_design_Read <= 1'b1;
        #5 ARES_design_CLK ^= 1;
        #5 ARES_design_CLK ^= 1;
        if (!(ARES_design_Empty === 1'b0)) begin
            $error("Failed on action=34 checking port FIFOGenerator.ARES_design.Empty with traceback /usr/local/lib/python3.7/dist-packages/fault/wrapper.py:62.  Expected %x, got %x.", 1'b0, ARES_design_Empty);
        end
        if (!(ARES_design_Full === 1'b0)) begin
            $error("Failed on action=35 checking port FIFOGenerator.ARES_design.Full with traceback /usr/local/lib/python3.7/dist-packages/fault/wrapper.py:62.  Expected %x, got %x.", 1'b0, ARES_design_Full);
        end
        if (!(ARES_design_RData === 32'd16)) begin
            $error("Failed on action=36 checking port FIFOGenerator.ARES_design.RData with traceback /usr/local/lib/python3.7/dist-packages/fault/wrapper.py:62.  Expected %x, got %x.", 32'd16, ARES_design_RData);
        end
        ARES_design_Read <= 1'b1;
        #5 ARES_design_CLK ^= 1;
        #5 ARES_design_CLK ^= 1;
        if (!(ARES_design_Empty === 1'b0)) begin
            $error("Failed on action=39 checking port FIFOGenerator.ARES_design.Empty with traceback /usr/local/lib/python3.7/dist-packages/fault/wrapper.py:62.  Expected %x, got %x.", 1'b0, ARES_design_Empty);
        end
        if (!(ARES_design_Full === 1'b0)) begin
            $error("Failed on action=40 checking port FIFOGenerator.ARES_design.Full with traceback /usr/local/lib/python3.7/dist-packages/fault/wrapper.py:62.  Expected %x, got %x.", 1'b0, ARES_design_Full);
        end
        if (!(ARES_design_RData === 32'd17)) begin
            $error("Failed on action=41 checking port FIFOGenerator.ARES_design.RData with traceback /usr/local/lib/python3.7/dist-packages/fault/wrapper.py:62.  Expected %x, got %x.", 32'd17, ARES_design_RData);
        end
        ARES_design_Read <= 1'b1;
        #5 ARES_design_CLK ^= 1;
        #5 ARES_design_CLK ^= 1;
        if (!(ARES_design_Empty === 1'b0)) begin
            $error("Failed on action=44 checking port FIFOGenerator.ARES_design.Empty with traceback /usr/local/lib/python3.7/dist-packages/fault/wrapper.py:62.  Expected %x, got %x.", 1'b0, ARES_design_Empty);
        end
        if (!(ARES_design_Full === 1'b0)) begin
            $error("Failed on action=45 checking port FIFOGenerator.ARES_design.Full with traceback /usr/local/lib/python3.7/dist-packages/fault/wrapper.py:62.  Expected %x, got %x.", 1'b0, ARES_design_Full);
        end
        if (!(ARES_design_RData === 32'd18)) begin
            $error("Failed on action=46 checking port FIFOGenerator.ARES_design.RData with traceback /usr/local/lib/python3.7/dist-packages/fault/wrapper.py:62.  Expected %x, got %x.", 32'd18, ARES_design_RData);
        end
        ARES_design_Read <= 1'b1;
        #5 ARES_design_CLK ^= 1;
        #5 ARES_design_CLK ^= 1;
        if (!(ARES_design_Empty === 1'b1)) begin
            $error("Failed on action=49 checking port FIFOGenerator.ARES_design.Empty with traceback /usr/local/lib/python3.7/dist-packages/fault/wrapper.py:62.  Expected %x, got %x.", 1'b1, ARES_design_Empty);
        end
        if (!(ARES_design_Full === 1'b0)) begin
            $error("Failed on action=50 checking port FIFOGenerator.ARES_design.Full with traceback /usr/local/lib/python3.7/dist-packages/fault/wrapper.py:62.  Expected %x, got %x.", 1'b0, ARES_design_Full);
        end
        ARES_design_Read <= 1'b0;
        #5 ARES_design_CLK ^= 1;
        #5 ARES_design_CLK ^= 1;
        #20 $finish;
    end

endmodule
