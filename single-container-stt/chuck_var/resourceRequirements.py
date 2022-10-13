class RapidResourceRequirement:
    resourceRequirement = {
        'marginalMem': 0.9 * 2 ** 30, # 900MB
        'marginalCpu': 60
    }

class RnntResourceRequirement:
    resourceRequirement = {
        'marginalMem': 0.06 * 2 ** 30,  # 60MB
        'marginalCpu': 12.5
    }
