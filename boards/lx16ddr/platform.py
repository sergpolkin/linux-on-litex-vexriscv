'''
http://blog.lambdaconcept.com/doku.php?id=products:lx16ddr
'''

from litex.build.generic_platform import *
from litex.build.xilinx import XilinxPlatform

_io = [
    ("clk50", 0, Pins("A10"), IOStandard("LVCMOS33")),

    ("user_led", 0, Pins("T9"), IOStandard("LVCMOS33"), Drive(24), Misc("SLEW=QUIETIO")), # D1
    ("user_led", 1, Pins("R9"), IOStandard("LVCMOS33"), Drive(24), Misc("SLEW=QUIETIO")), # D3

    ("user_btn", 0, Pins("T8"), IOStandard("LVCMOS33")), # SW2
    ("user_btn", 1, Pins("R7"), IOStandard("LVCMOS33")), # SW3

    ("serial", 0,
        Subsignal("tx", Pins("P12"), Misc("SLEW=SLOW")),
        Subsignal("rx", Pins("M11"), Misc("PULLUP")),
        IOStandard("LVCMOS33")
    ),

    ("spiflash", 0,
        Subsignal("cs_n", Pins("T3")),
        Subsignal("clk", Pins("R11")),
        Subsignal("mosi", Pins("T10")),
        Subsignal("miso", Pins("P10"), Misc("PULLUP")),
        IOStandard("LVCMOS33"), Misc("SLEW=FAST")
    ),

    ("ddram_clock", 0,
        # mcb3_dram_ck, mcb3_dram_ck_n
        Subsignal("p", Pins("E2")),
        Subsignal("n", Pins("E1")),
        IOStandard("DIFF_SSTL15_II"),
    ),
    ("ddram", 0,
        # mcb3_dram_a
        Subsignal("a", Pins(
            "K5 K6 D1 L4 G5 H4 H3 D3",
            "B2 A2 G6 E3 F3 F6 F5"),
            IOStandard("SSTL15_II")),
        # mcb3_dram_ba
        Subsignal("ba", Pins("C3 C2 B1"), IOStandard("SSTL15_II")),
        # mcb3_dram_ras_n
        Subsignal("ras_n", Pins("J6"), IOStandard("SSTL15_II")),
        # mcb3_dram_cas_n
        Subsignal("cas_n", Pins("H5"), IOStandard("SSTL15_II")),
        # mcb3_dram_we_n
        Subsignal("we_n", Pins("C1"), IOStandard("SSTL15_II")),
        # mcb3_dram_dm, mcb3_dram_udm
        Subsignal("dm", Pins("J4 K3"), IOStandard("SSTL15_II")),
        # mcb3_dram_dq
        Subsignal("dq", Pins(
            "K2 K1 J3 J1 F2 F1 G3 G1",
            "L3 L1 M2 M1 P2 P1 R2 R1"),
            IOStandard("SSTL15_II")),
        # mcb3_dram_dqs, mcb3_dram_udqs
        Subsignal("dqs",   Pins("H2 N3"), IOStandard("DIFF_SSTL15_II")),
        # mcb3_dram_dqs_n, mcb3_dram_udqs_n
        Subsignal("dqs_n", Pins("H1 N1"), IOStandard("DIFF_SSTL15_II")),
        # mcb3_dram_cke
        Subsignal("cke", Pins("F4"), IOStandard("SSTL15_II")),
        # mcb3_dram_odt
        Subsignal("odt", Pins("L5"), IOStandard("SSTL15_II")),
        # mcb3_dram_reset_n
        Subsignal("reset_n", Pins("E4"), IOStandard("LVCMOS15")),
        # mcb3_rzq
        # Subsignal("rzq", Pins("M4"), IOStandard("SSTL15_II")),
        # mcb3_zio
        # Subsignal("zio", Pins("M5"), IOStandard("SSTL15_II")),
    ),
]

_connectors = [
    #      |0              |4              |8              |12             |16             |20             |24
    ("A", "E12 B15 C15 D14 E15 F15 G11 F14 G16 H15 G12 H13 J14 J11 K14 K15 L16 K11 M15 N14 M13 L12 P15 R15 R14 T13 T12"), # U7 1
    ("B", "E13 B16 C16 D16 E16 F16 F12 F13 G14 H16 H11 H14 J16 J12 J13 K16 L14 K12 M16 N16 M14 L13 P16 R16 T15 T14 R12"), # U7 2
    ("C", "A14 C13 B12 C11 B10 C9  B8  C7  B6  B5  E10 E11 F9  C8  E7  F7  D6  M7  N8  P9  T5  T6  N9  L8  L10 P12 R9"),  # U8 1
    ("D", "B14 A13 A12 A11 A9  A8  A7  A6  A5  A4  C10 F10 D9  D8  E6  C6  N6  P6  L7  T4  R5  T7  M9  M10 P11 M11 T9"),  # U8 2
]

class Platform(XilinxPlatform):
    default_clk_name = "clk50"
    default_clk_period = 20.0

    def __init__(self):
        XilinxPlatform.__init__(self, "xc6slx16-ftg256-2", _io, _connectors)
        self.add_platform_command("""CONFIG VCCAUX=3.3;""")
