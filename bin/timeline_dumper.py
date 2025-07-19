#!/usr/bin/env python3

from re import compile
from sys import argv

input = argv[1]

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
