import React from "react";

import classes from "./Progress.module.scss";
import { RingProgress } from "@mantine/core";
import { ProgressProps } from "./ProgressTypes";

export function Progress({ on, total, label, title, onClick }: ProgressProps) {
  return (
    <span data-testid="LocalProgress">
      <RingProgress
        size={56}
        thickness={8}
        onClick={onClick}
        title={title}
        label={
          <div onClick={onClick} className={classes.label}>
            {label}
          </div>
        }
        sections={[
          { value: ((on + 1) / total) * 100, color: "var(--secondary-color)" },
        ]}
        data-testid="Progress"
      />
    </span>
  );
}
