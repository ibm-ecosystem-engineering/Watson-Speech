class WTTSDnnResourceRequirement:
    resourceRequirement = {
        'marginalMem' : 250*2**20, # 130 MB
        'marginalCpu' : 40
    }
class WTTSLargeVoiceResourceRequirement:
    resourceRequirement = {
        'marginalMem' : 600*2**20, # 600 MB
        'marginalCpu': 20
    }
