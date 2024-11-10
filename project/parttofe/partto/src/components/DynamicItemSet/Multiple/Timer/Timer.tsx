import React, { useEffect, useState } from "react";

import { DateTime, Duration, getDateTime } from "../../../../api/helpers";
import { Progress } from "../Progress/Progress";

export interface TimerProps {
  start: DateTime;
  duration: Duration;
  label: string;
  title: string;
  onClick: () => void;
}

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
