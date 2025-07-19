import { Duration, getDuration } from "./duration";

export enum Format {
  TIME,
}

export interface DateTime {
  sinceEpoch: () => number;
  toISOString: () => string;
  add: (arg: Duration) => DateTime;
  subtract: (arg: DateTime) => Duration;
  format: (format: Format) => string;
}

export function getDateTime(inDate?: Date): DateTime {
  const date = inDate || new Date();

  return {
    sinceEpoch: () => date.getTime(),
    toISOString: () => date.toISOString(),
    format: (format: Format) => {
      const timeWithZone = date
        .toLocaleString("en-US", { timeZoneName: "short" })
        .split(",")[1]
        .trim()
        .split(" ");
      const numbers = timeWithZone[0].split(":");
      numbers.pop();
      return [numbers.join(":"), timeWithZone[1]].join(" ");
    },
    add: (duration: Duration) =>
      getDateTime(new Date(date.getTime() + duration.toMilliseconds())),
    subtract: (subtrahend: DateTime) =>
      getDuration(date.getTime() - subtrahend.sinceEpoch()),
  };
}
