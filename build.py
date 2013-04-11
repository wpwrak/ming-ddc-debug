from migen.fhdl.structure import *
from migen.fhdl.module import Module
from mibuild.platforms import m1

from edid import EDID

class EDIDTester(Module):
	def __init__(self, clk50_pad, rst_pad, dvi_pads, led_pad,
	    x0, x1, x2, x3):
		self.clock_domains.cd_sys = ClockDomain("sys")
		self.clock_domains.cd_pix = ClockDomain("pix")
		self.comb += [
			self.cd_sys.clk.eq(clk50_pad),
			self.cd_sys.rst.eq(rst_pad),
			self.cd_pix.clk.eq(dvi_pads.clk)
		]

		self.submodules.edid = EDID(dvi_pads)

		counter = Signal(23)
		self.comb += led_pad.eq(counter[22])
		self.sync.pix += counter.eq(counter + 1)
		self.comb += Cat(*(x0, x1, x2, x3)).eq(counter[8:12])
#		self.comb += x0.eq(counter[10])
#		self.comb += x1.eq(counter[12])
#		self.comb += x2.eq(counter[14])
#		self.comb += x3.eq(counter[16])

plat = m1.Platform()
dvi_pads = plat.request("dvi_in", 0)
x = plat.request("mmc", 0)
dut = EDIDTester(plat.request("clk50"), plat.request("user_btn", 0),
	dvi_pads, plat.request("user_led", 0),
	x.dat1, x.clk, x.cmd, x.dat3)
plat.add_platform_command("NET \"{clk}\" CLOCK_DEDICATED_ROUTE = FALSE;", clk=dvi_pads.clk)
plat.build_cmdline(dut)
