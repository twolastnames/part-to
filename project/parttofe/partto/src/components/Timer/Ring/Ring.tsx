import React from "react";

import classes from "./Ring.module.scss";
import { RingProps } from "./RingTypes";
import { RingProgress } from "@mantine/core";

export function Ring({ magnitude, label }: RingProps) {
  const color1 =
    magnitude >= 1 ? "var(--highlight-color)" : "var(--secondary-color)";
  const value1 = magnitude >= 2 ? 1 : magnitude % 1;
  const color2 =
    magnitude >= 1 ? "var(--secondary-color)" : "var(--highlight-color)";
  const value2 = magnitude >= 2 ? 0 : 1 - (magnitude % 1);

  return (
    <div className={classes.ring} data-testid="Ring">
      <RingProgress
        size={100}
        thickness={100}
        sections={[
          { color: color1, value: value1 * 100 },
          { color: color2, value: value2 * 100 },
        ]}
      />
      <div className={classes.label}>{label}</div>
    </div>
  );
}
