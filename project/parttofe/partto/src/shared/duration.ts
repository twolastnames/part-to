export interface Duration {
  toMilliseconds: () => number;
  add: (addend: Duration) => Duration;
  subtract: (subtrahend: Duration) => Duration;
  toString: () => string;
  format: (formatter: keyof DurationFormats) => string;
}

type DurationFormatter = (
  negative: boolean,
  hours: number,
  minutes: number,
  seconds: number,
) => string;

const durationFormatter =
  (
    hourFormatter: (isFirst: boolean, arg: number) => string,
    minuteFormatter: (isFirst: boolean, arg: number) => string,
    secondFormatter: (isFirst: boolean, arg: number) => string,
    joiner: (negative: boolean, arg: Array<string>) => string,
  ) =>
  (negative: boolean, hours: number, minutes: number, seconds: number) => {
    const stringValues = [
      { value: hours, formatter: hourFormatter },
      { value: minutes, formatter: minuteFormatter },
      { value: seconds, formatter: secondFormatter },
    ].reduce(
      (current: Array<string>, { value, formatter }) =>
        current.length > 0
          ? [...current, formatter(false, value)]
          : value === 0
            ? current
            : [formatter(true, value)],
      [],
    );
    return joiner(negative, stringValues);
  };

const timerValueStringer = (_: boolean, value: number) => value.toString();
const timerValuePadder = (isFirst: boolean, value: number) =>
  isFirst ? value.toString() : value.toString().padStart(2, "0");

export enum DurationFormat {
  TIMER = "timer",
  LONG = "long",
  SHORT = "short",
}

type DurationFormats = { [key in DurationFormat]: DurationFormatter };

const joinShort = (negative: boolean, values: Array<string>) =>
  `${negative ? "minus " : ""}${
    [
      "",
      `${values[0]}`,
      `${values[0]} & ${values[1]}`,
      `${values[0]}, ${values[1]} & ${values[2]}`,
    ][values.length || 0]
  }`;

const joinLong = (negative: boolean, values: Array<string>) =>
  `${negative ? "negative " : ""}${
    [
      "",
      `${values[0]}`,
      `${values[0]} and ${values[1]}`,
      `${values[0]}, ${values[1]}, and ${values[2]}`,
    ][values.length || 0]
  }`;

export const durationFormatters: DurationFormats = {
  [DurationFormat.TIMER]: durationFormatter(
    timerValueStringer,
    timerValuePadder,
    timerValuePadder,
    (negative, values) => `${negative ? "-" : ""}${values.join(" : ")}`,
  ),
  [DurationFormat.LONG]: durationFormatter(
    (_, value) => `${value} hour${value === 1 ? "" : "s"}`,
    (_, value) => `${value} minute${value === 1 ? "" : "s"}`,
    (_, value) => `${value} second${value === 1 ? "" : "s"}`,
    joinLong,
  ),
  [DurationFormat.SHORT]: durationFormatter(
    (_, value) => `${value} hr`,
    (_, value) => `${value} min`,
    (_, value) => `${value} sec`,
    joinShort,
  ),
};

const getDisplayableDuration = (
  millis: number,
  formatterIn?: keyof DurationFormats,
) => {
  const formatter = formatterIn
    ? durationFormatters[formatterIn]
    : durationFormatters.short;
  const negative = millis < 0;
  const seconds = Math.round(Math.abs(millis / 1000) % 60);
  const minutes = Math.floor(Math.abs(millis / 60000) % 60);
  const hours = Math.floor(Math.abs(millis / (60 * 60000)));
  return formatter(negative, hours, minutes, seconds);
};

const formatDuration = (value: number, formatter?: keyof DurationFormats) =>
  getDisplayableDuration(value, formatter);

export const getDuration: (arg: number) => Duration = (value) => ({
  toMilliseconds: () => value,
  add: (addend: Duration) => getDuration(value + addend.toMilliseconds()),
  subtract: (subtrahend: Duration) =>
    getDuration(value + subtrahend.toMilliseconds()),
  format: (formatter?: keyof DurationFormats) =>
    formatDuration(value, formatter),
  toString: () => formatDuration(value),
});
