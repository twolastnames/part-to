def handle(arguments):
    """return body here"""
    return arguments.respond_200(
        {
            "estimatedDuration": arguments.task.duration,
            "from": [],
            "initialEstimation": {
                "duration": arguments.task.duration,
                "usedInCalculation": True,
            },
        }
    )
