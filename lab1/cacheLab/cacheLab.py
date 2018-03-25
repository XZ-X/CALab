import m5
from m5.objects import *
from caches import *
from optparse import OptionParser

#parse the cli args

parser = OptionParser()
parser.add_option('--l1isz', help="L1 instruction cache size")
parser.add_option('--l1dsz', help="L1 data cache size")
parser.add_option('--l2sz', help="Unified L2 cache size")
parser.add_option('--clk',help="clock cycle frequency")

(options, args) = parser.parse_args()



system = System()
system.clk_domain = SrcClockDomain()

if options and options.clk:
	system.clk_domain.clock = options.clk
else:
	system.clk_domain.clock= '1GHz'

system.clk_domain.voltage_domain = VoltageDomain()

# mem

system.mem_mode= 'timing'
system.mem_ranges = [AddrRange('512MB')]

#CPU

system.cpu=TimingSimpleCPU()

#bus 

system.membus = SystemXBar()

#cache

system.cpu.icache= L1ICache(options)
system.cpu.dcache= L1DCache(options)
system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

# L2Cache
system.l2bus = L2XBar()

system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)
system.l2cache = L2Cache(options)
system.l2cache.connectCPUSideBus(system.l2bus)

system.l2cache.connectMemSideBus(system.membus)

#IO

system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.master
system.cpu.interrupts[0].int_master = system.membus.slave
system.cpu.interrupts[0].int_slave = system.membus.master

system.system_port = system.membus.slave

# memController
system.mem_ctr1 = DDR3_1600_8x8()
system.mem_ctr1.range = system.mem_ranges[0]
system.mem_ctr1.port = system.membus.master


process = Process()
process.cmd = ['tests/test-progs/hello/bin/x86/linux/hello']
system.cpu.workload = process
system.cpu.createThreads()

root = Root(full_system = False, system = system)
m5.instantiate()


print("begin")
exit_event = m5.simulate()

print('Exiting @ tick {} because {}'
      .format(m5.curTick(), exit_event.getCause()))
