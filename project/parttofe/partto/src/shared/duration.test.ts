import { expect, test } from "@jest/globals";
import { DurationFormat, getDuration } from "./duration";

[
  {
    multiplier: 1,
    hours: 0,
    minutes: 0,
    seconds: 15,
    timerDisplay: "15",
    shortDisplay: "15 sec",
    longDisplay: "15 seconds",
  },
  {
    multiplier: 1,
    hours: 0,
    minutes: 0,
    seconds: 1,
    timerDisplay: "1",
    shortDisplay: "1 sec",
    longDisplay: "1 second",
  },
  {
    multiplier: 1,
    hours: 0,
    minutes: 15,
    seconds: 0,
    timerDisplay: "15 : 00",
    shortDisplay: "15 min & 0 sec",
    longDisplay: "15 minutes and 0 seconds",
  },
  {
    multiplier: -1,
    hours: 0,
    minutes: 1,
    seconds: 1,
    timerDisplay: "-1 : 01",
    shortDisplay: "minus 1 min & 1 sec",
    longDisplay: "negative 1 minute and 1 second",
  },
  {
    multiplier: 1,
    hours: 14,
    minutes: 0,
    seconds: 45,
    timerDisplay: "14 : 00 : 45",
    shortDisplay: "14 hr, 0 min & 45 sec",
    longDisplay: "14 hours, 0 minutes, and 45 seconds",
  },
].forEach(
  ({
    multiplier,
    hours,
    minutes,
    seconds,
    timerDisplay,
    shortDisplay,
    longDisplay,
  }) => {
    const duration = getDuration(
      multiplier * (seconds * 1000 + minutes * 60000 + hours * 60 * 60000),
    );

    test(`${hours} hours, ${minutes} minutes, & ${seconds} seconds timer dipsays ${timerDisplay}`, () => {
      expect(duration.format(DurationFormat.TIMER)).toEqual(timerDisplay);
    });

    test(`${hours} hours, ${minutes} minutes, & ${seconds} seconds timer dipsays ${timerDisplay}`, () => {
      expect(duration.format(DurationFormat.SHORT)).toEqual(shortDisplay);
    });

    test(`${hours} hours, ${minutes} minutes, & ${seconds} seconds timer dipsays ${timerDisplay}`, () => {
      expect(duration.format(DurationFormat.LONG)).toEqual(longDisplay);
    });
  },
);
