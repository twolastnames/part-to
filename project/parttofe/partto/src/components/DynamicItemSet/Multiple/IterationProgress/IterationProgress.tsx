import React from "react";

import classes from "./IterationProgress.module.scss";
import { Count } from "../Count/Count";
import { Timer } from "../Timer/Timer";
import { getDateTime, getDuration } from "../../../../api/helpers";
import { Slider } from "@mantine/core";

export interface IterationProgressProps {
  showDuration: number;
  total: number;
  setShowDuration: (arg: number) => void;
  on: number;
}

export const marks = [
  { label: "1 seconds", duration: getDuration(1000) },
  { label: "2 seconds", duration: getDuration(2000) },
  { label: "4 seconds", duration: getDuration(4000) },
  { label: "8 seconds", duration: getDuration(8000) },
  { label: "16 seconds", duration: getDuration(16000) },
  { label: "Paused", duration: getDuration(99999999999999999) },
].map(({ label, duration }, value) => ({ value, label, duration }));

export function IterationProgress({
  total,
  showDuration,
  setShowDuration,
  on,
}: IterationProgressProps) {
  return (
    <div className={classes.iterationProgress} data-testid="IterationProgress">
      <span>
        <Timer
          key={on}
          start={getDateTime()}
          duration={marks[showDuration].duration}
          label={(on + 1).toString()}
        />
      </span>
      <span className={classes.count}>
        <Count total={total} on={on} />
      </span>
      <span className={classes.slider}>
        <Slider
          label={(value) =>
            (
              marks.find((mark) => mark.value === value) || {
                label: "undefined",
              }
            ).label
          }
          defaultValue={marks[2].value}
          min={0}
          max={5}
          step={1}
          marks={marks}
          styles={{ markLabel: { display: "none" } }}
          color="indigo"
          onChangeEnd={setShowDuration}
        />
      </span>
    </div>
  );
}
