import React from "react";

import classes from "./IterationProgress.module.scss";
import { Count } from "../Count/Count";
import { Timer } from "../Timer/Timer";
import { IterationProgressProps } from "./IterationProgressTypes";
import { DurationFormat } from "../../../../shared/duration";
import { getDateTime } from "../../../../shared/dateTime";
import { useSingleOfPair } from "../../../../providers/DynamicItemSetPair";

export function IterationProgress({ context }: IterationProgressProps) {
  const {
    nextShowDuration,
    showDuration,
    paused,
    selected,
    getTotal,
    togglePause,
  } = useSingleOfPair(context);
  const timerDuration = paused ? undefined : showDuration;
  const countTitle = showDuration.format(DurationFormat.LONG);
  return (
    <div className={classes.iterationProgress} data-testid="IterationProgress">
      <span>
        <Timer
          key={selected}
          start={getDateTime()}
          duration={timerDuration}
          label={(selected + 1).toString()}
          title={paused ? "Paused" : "Unpaused"}
          onClick={togglePause}
        />
      </span>
      <span className={classes.count}>
        <Count
          onClick={nextShowDuration}
          title={countTitle}
          total={getTotal()}
          on={selected}
        />
      </span>
    </div>
  );
}
