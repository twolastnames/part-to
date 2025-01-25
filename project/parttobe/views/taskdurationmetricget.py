def handle(arguments):
    """return body here"""
    return {
        "estimatedDuration": arguments.task.duration,
        "from": [],
        "initialEstimation": {
            "duration": arguments.task.duration,
            "usedInCalculation": True,
        },
    }
