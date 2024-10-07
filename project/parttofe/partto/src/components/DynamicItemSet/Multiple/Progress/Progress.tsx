import React from "react";

import classes from "./Progress.module.scss";
import { RingProgress } from "@mantine/core";

export interface ProgressProps {
  on: number;
  total: number;
  label: string;
}

export function Progress({ on, total, label }: ProgressProps) {
  return (
    <span data-testid="LocalProgress">
      <RingProgress
        size={72}
        label={<div className={classes.label}>{label}</div>}
        sections={[
          { value: ((on + 1) / total) * 100, color: "var(--secondary-color)" },
        ]}
        data-testid="Progress"
      />
    </span>
  );
}
