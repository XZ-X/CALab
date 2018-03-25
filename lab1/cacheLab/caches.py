from m5.objects import Cache

class L1Cache(Cache):
    assoc = 2
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 4
    tgts_per_mshr = 20
    def connectBus(self, bus):
    	self.mem_side = bus.slave
    def __init__(self, options=None):
    	super(L1Cache, self).__init__()
    	pass

class L1ICache(L1Cache):
    size = '16kB'

    def __init__(self, options=None):
    	super(L1ICache, self).__init__(options)
    	if not options or not options.l1isz:
        	return
    	self.size = options.l1isz
    
    def connectCPU(self,cpu):
	self.cpu_side = cpu.icache_port

class L1DCache(L1Cache):
    size = '64kB'

    def __init__(self, options=None):
    	super(L1DCache, self).__init__(options)
    	if not options or not options.l1dsz:
        	return
    	self.size = options.l1dsz


    def connectCPU(self,cpu):
	self.cpu_side = cpu.dcache_port


class L2Cache(Cache):
    size = '256kB'
    assoc = 8
    tag_latency = 20
    data_latency = 20
    response_latency = 20
    mshrs = 20
    tgts_per_mshr = 12

    def __init__(self, options=None):
    	super(L2Cache, self).__init__()
    	if not options or not options.l2sz:
        	return
    	self.size = options.l2sz
    def connectCPUSideBus(self, bus):
    	self.cpu_side = bus.master

    def connectMemSideBus(self, bus):
    	self.mem_side = bus.slave
