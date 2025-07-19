import { expect, describe, it } from "@jest/globals";
import { Format, getDateTime } from "./dateTime";
import { getDuration } from "./duration";

describe("DateTime", () => {
  beforeAll(() => {
    jest.useFakeTimers();
  });
  afterAll(() => {
    jest.useRealTimers();
  });
  it("picks now", () => {
    jest.setSystemTime(new Date("April 27, 1989 9:00 AM"));
    expect(getDateTime().sinceEpoch()).toEqual(new Date().getTime());
  });
});

test("addition", () => {
  expect(
    getDateTime(new Date("April 27, 1989 9:00 AM"))
      .add(getDuration(5 * 60 * 1000))
      .sinceEpoch(),
  ).toEqual(new Date("April 27, 1989 9:05 AM").getTime());
});

test("duration subtraction", () => {
  expect(
    getDateTime(new Date("April 27, 1989 9:00 AM"))
      .add(getDuration(-5 * 60 * 1000))
      .sinceEpoch(),
  ).toEqual(new Date("April 27, 1989 8:55 AM").getTime());
});

test("format short time", () => {
  expect(
    getDateTime(new Date("April 27, 1989 9:00 AM"))
      .subtract(getDateTime(new Date("April 27, 1989 8:55 AM")))
      .toMilliseconds(),
  ).toEqual(getDuration(5 * 60 * 1000).toMilliseconds());
});

test("date subtraction", () => {
  expect(
    getDateTime(new Date("April 27, 1989 9:31 AM")).format(Format.TIME),
  ).toEqual("9:31 AM");
});
