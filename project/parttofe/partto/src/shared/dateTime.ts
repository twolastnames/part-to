import { Duration, getDuration } from "./duration";

export interface DateTime {
  sinceEpoch: () => number;
  toISOString: () => string;
  add: (arg: Duration) => DateTime;
  subtract: (arg: DateTime) => Duration;
}

export function getDateTime(inDate?: Date): DateTime {
  const date = inDate || new Date();

  return {
    sinceEpoch: () => date.getTime(),
    toISOString: () => date.toISOString(),
    add: (duration: Duration) =>
      getDateTime(new Date(date.getTime() + duration.toMilliseconds())),
    subtract: (subtrahend: DateTime) =>
      getDuration(date.getTime() - subtrahend.sinceEpoch()),
  };
}
