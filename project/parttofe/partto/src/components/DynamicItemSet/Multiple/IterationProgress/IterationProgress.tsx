import React, { useEffect, useRef } from "react";

import classes from "./IterationProgress.module.scss";
import { Count } from "../Count/Count";
import { Timer } from "../Timer/Timer";
import { getDateTime, getDuration } from "../../../../api/helpers";
import { IterationProgressProps } from "./IterationProgressTypes";

export const speeds = [
  { label: "1 Seconds", duration: getDuration(1000) },
  { label: "2 Seconds", duration: getDuration(2000) },
  { label: "4 Seconds", duration: getDuration(4000) },
  { label: "8 Seconds", duration: getDuration(8000) },
  { label: "16 Seconds", duration: getDuration(16000) },
  { label: "Paused", duration: getDuration(99999999999999999) },
].map(({ label, duration }, value) => ({ value, label, duration }));

export function IterationProgress({
  total,
  showDuration,
  setShowDuration,
  paused,
  setPaused,
  on,
}: IterationProgressProps) {
  const lastDuration = useRef<number>(showDuration);
  useEffect(() => {
    if (showDuration !== speeds.length - 1) {
      lastDuration.current = showDuration;
    }
  }, [showDuration]);
  const timerDuration = (
    paused ? speeds[speeds.length - 1] : speeds[showDuration]
  ).duration;
  const countTitle = speeds[(showDuration + 1) % (speeds.length - 1)].label;
  return (
    <div className={classes.iterationProgress} data-testid="IterationProgress">
      <span>
        <Timer
          key={on}
          start={getDateTime()}
          duration={timerDuration}
          label={(on + 1).toString()}
          title={paused ? "Unpause" : "Pause"}
          onClick={() => {
            setPaused(!paused);
          }}
        />
      </span>
      <span className={classes.count}>
        <Count
          onClick={() => {
            setShowDuration((lastDuration.current + 1) % (speeds.length - 1));
          }}
          title={countTitle}
          total={total}
          on={on}
        />
      </span>
    </div>
  );
}
