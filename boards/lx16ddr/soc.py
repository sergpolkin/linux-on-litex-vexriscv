from migen import *

from litex.build.generic_platform import *
from litex.soc.integration.soc_core import *

from litedram.modules import MT41J128M16
from litedram.phy import s6ddrphy

from .crg import _CRG
from .platform import Platform


class BaseSoC(SoCCore):
    def __init__(self, sys_clk_freq=int(50e6), **kwargs):
        platform = Platform()

        # SoCCore ----------------------------------------------------------------------------------
        SoCCore.__init__(self, platform, sys_clk_freq, ident="LiteX SoC on LX16DDR", **kwargs)

        # CRG --------------------------------------------------------------------------------------
        self.submodules.crg = _CRG(platform, sys_clk_freq)
        self.platform.add_period_constraint(self.crg.cd_sys.clk, 20.0)
        self.platform.add_period_constraint(self.crg.cd_sys2x.clk, 10.0)
        self.platform.add_period_constraint(self.crg.cd_sdram_half.clk, 5.0)
        self.platform.add_period_constraint(self.crg.cd_sdram_full_wr.clk, 5.0)
        self.comb += self.crg.reset.eq(~platform.request("user_btn"))

        # DDR3 SDRAM -------------------------------------------------------------------------------
        self.submodules.ddrphy = s6ddrphy.S6QuarterRateDDRPHY(platform.request("ddram"),
            rd_bitslip        = 0,
            wr_bitslip        = 4,
            dqs_ddr_alignment = "C0")
        self.add_csr("ddrphy")
        self.add_sdram("sdram",
            phy           = self.ddrphy,
            module        = MT41J128M16(sys_clk_freq, "1:4"),
            l2_cache_size = kwargs.get("l2_size", 2*1024),
        )
        self.comb += [
            self.ddrphy.clk8x_wr_strb.eq(self.crg.clk8x_wr_strb),
            self.ddrphy.clk8x_rd_strb.eq(self.crg.clk8x_rd_strb),
        ]
