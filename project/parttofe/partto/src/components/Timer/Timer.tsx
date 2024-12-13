import React, { useEffect, useState } from "react";

import classes from "./Timer.module.scss";
import { TimerProps } from "./TimerTypes";
import { Ring } from "./Ring/Ring";
import { DateTime, getDateTime } from "../../shared/dateTime";
import { Duration, DurationFormat } from "../../shared/duration";

const getMagnitude = (started: DateTime, duration: Duration) =>
  (getDateTime().sinceEpoch() - started.sinceEpoch()) /
  duration.toMilliseconds();

export function Timer({ start, duration }: TimerProps) {
  const [started] = useState<DateTime>(start || getDateTime());

  const [magnitude, setMagnitude] = useState<number>(
    getMagnitude(started, duration),
  );

  useEffect(() => {
    const listener = () => {
      setMagnitude(getMagnitude(started, duration));
    };
    const id = setInterval(listener, 1000);
    return () => {
      clearInterval(id);
    };
  }, [started, duration]);

  return (
    <Ring
      label={
        <div className={magnitude > 2 ? classes.overdue : classes.normal}>
          {started
            .add(duration)
            .subtract(getDateTime())
            .format(DurationFormat.TIMER)}
        </div>
      }
      magnitude={magnitude}
    />
  );
}
