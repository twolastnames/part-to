import React, { ReactElement, useEffect, useState } from "react";

import { TimerStringProps } from "./TimerStringTypes";
import { getDateTime } from "../../../../shared/dateTime";
import { DurationFormat } from "../../../../shared/duration";

export function TimerString({
  started,
  duration,
}: TimerStringProps): ReactElement {
  const [key, setKey] = useState<number>(Math.random());
  useEffect(() => {
    const id = setInterval(() => {
      setKey(Math.random());
    }, 1000);
    return () => {
      clearInterval(id);
    };
  }, []);
  return (
    <span key={key}>
      {started
        .add(duration)
        .subtract(getDateTime())
        .format(DurationFormat.LONG)}
    </span>
  );
}
