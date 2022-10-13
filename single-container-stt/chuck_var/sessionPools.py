class PreWarmingPolicy:
    sessionPool = {
        'minWarmSessions': 1,
        'maxUseCount': 1000
    }

class NoPreWarmingPolicy:
    sessionPool = {
        'maxUseCount': 1000
    }

class DefaultPolicy:
    sessionPool = {}
