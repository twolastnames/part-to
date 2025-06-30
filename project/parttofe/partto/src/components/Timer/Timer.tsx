import React, { ReactNode, useEffect, useRef, useState } from "react";

import classes from "./Timer.module.scss";
import { TimerProps } from "./TimerTypes";
import { Ring } from "./Ring/Ring";
import { DateTime, getDateTime } from "../../shared/dateTime";
import { Duration, DurationFormat, getDuration } from "../../shared/duration";
import { Flasher } from "../Flasher/Flasher";
import { AdjustableDigit } from "./AdjustableDigit/AdjustableDigit";

const adders = [1000, 10000, 60000, 600000, 60 * 60 * 1000];

const getEnforcedDurationLabel = (
  duration: string,
  addOffset: (offset: Duration) => void,
) => (
  <>
    {
      duration
        .split("")
        .reverse()
        .reduce(
          (
            { result, adder }: { result: Array<ReactNode>; adder: number },
            character: string,
          ) => {
            const parsed = parseInt(character);
            return {
              adder: isNaN(parsed) ? adder : adder + 1,
              result: [
                isNaN(parsed) ? (
                  <span>{character}</span>
                ) : (
                  <AdjustableDigit
                    increment={
                      adders.length <= adder
                        ? undefined
                        : () => {
                            addOffset(getDuration(adders[adder]));
                          }
                    }
                    decrement={
                      adders.length <= adder
                        ? undefined
                        : () => {
                            addOffset(getDuration(-adders[adder]));
                          }
                    }
                  >
                    {character}
                  </AdjustableDigit>
                ),
                ...result,
              ],
            };
          },
          { adder: 0, result: [] },
        ).result
    }
  </>
);

const getMagnitude = (started: DateTime, duration: Duration) =>
  (getDateTime().sinceEpoch() - started.sinceEpoch()) /
  duration.toMilliseconds();

export function Timer({
  start,
  duration,
  adjustment,
  ringClasses,
}: TimerProps) {
  const [rerenderKey, setRerenderKey] = useState<number>(Math.random());
  const [started] = useState<DateTime>(start || getDateTime());
  const offset = useRef(adjustment ? adjustment.offset : getDuration(0));
  const addOffset = (value: Duration) => {
    offset.current = offset.current.add(value);
    adjustment?.setOffset(offset.current);
  };

  const getEffectiveDuration = () => duration.add(offset.current);
  const [magnitude, setMagnitude] = useState<number>(
    getMagnitude(started, getEffectiveDuration()),
  );

  useEffect(() => {
    const listener = () => {
      setMagnitude(getMagnitude(started, getEffectiveDuration()));
      setRerenderKey(Math.random());
    };
    const id = setInterval(listener, 1000);
    return () => {
      clearInterval(id);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [duration, started]);

  const labelText = started
    .add(getEffectiveDuration())
    .subtract(getDateTime())
    .format(DurationFormat.TIMER);

  const label = adjustment
    ? getEnforcedDurationLabel(labelText, addOffset)
    : labelText;
  return (
    <Ring
      key={rerenderKey}
      label={
        <span className={classes.label}>
          {magnitude > 2 ? <Flasher>{label}</Flasher> : label}
        </span>
      }
      classNames={ringClasses}
      magnitude={magnitude}
    />
  );
}
