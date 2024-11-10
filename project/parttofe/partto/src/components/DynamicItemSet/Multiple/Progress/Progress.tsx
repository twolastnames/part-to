import React from "react";

import classes from "./Progress.module.scss";
import { RingProgress } from "@mantine/core";

export interface ProgressProps {
  on: number;
  total: number;
  label: string;
  title: string;
  onClick: () => void;
}

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
