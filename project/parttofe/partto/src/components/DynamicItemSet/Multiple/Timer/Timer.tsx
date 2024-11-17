import React, { useEffect, useState } from "react";

import { Progress } from "../Progress/Progress";
import { TimerProps } from "./TimerTypes";
import { getDateTime } from "../../../../shared/dateTime";

export function Timer({ start, duration, label, title, onClick }: TimerProps) {
  const [on, setOn] = useState<number>(0);
  useEffect(() => {
    const id = setInterval(() => {
      const now = getDateTime();
      setOn(now.subtract(start).toMilliseconds());
    }, 100);
    return () => {
      clearInterval(id);
    };
  }, [start]);
  return (
    <span data-testid="Timer">
      <Progress
        onClick={onClick}
        title={title}
        label={label}
        on={on}
        total={duration.toMilliseconds()}
      />
    </span>
  );
}
