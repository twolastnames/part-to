#!/usr/bin/env python3

from re import compile
from sys import argv

input = argv[1]


# input = "Marker-id=[id=1:duration=0:00:06:engagement=None]:till=0:00:00:is_done=False, Marker-id=[id=4:duration=0:01:00:engagement=0.25]:till=0:00:00:is_done=False, Marker-id=[id=1:duration=0:00:06:engagement=None]:till=0:00:08:is_done=True, Marker-id=[id=2:duration=0:00:20:engagement=None]:till=0:00:08:is_done=False, Marker-id=[id=3:duration=0:00:20:engagement=0.1]:till=0:00:13.333333:is_done=False, Marker-id=[id=3:duration=0:00:20:engagement=0.1]:till=0:00:33.333333:is_done=True, Marker-id=[id=2:duration=0:00:20:engagement=None]:till=0:00:37.333333:is_done=True, Marker-id=[id=4:duration=0:01:00:engagement=0.25]:till=0:01:00:is_done=True"


pattern = compile(
    "Marker-id=\[id=(?P<id>[^:]+):duration=(?P<durationH>[^:]+):(?P<durationM>[^:]+):(?P<durationS>[^:]+):engagement=[^\]]+\]:till=(?P<tillH>[^:]+):(?P<tillM>[^:]+):(?P<tillS>[^:]+):is_done=(?P<done>\\w+)"
)


def get_seconds(hours, minutes, seconds):
    return str(round(float(hours) * 60 * 60 + float(minutes) * 60 + float(seconds), 6))


parts = [part.strip() for part in input.split(",")]


for part, index in zip(parts, range(len(parts))):
    result = pattern.match(part)
    till = get_seconds(result["tillH"], result["tillM"], result["tillS"])
    print(
        "self.assertEqual(line[{index}], Marker({id}, timedelta(seconds={till}), {done}))".format(
            index=index,
            till=till,
            id=result["id"],
            done=result["done"],
        )
    )
    # print(part, till)
