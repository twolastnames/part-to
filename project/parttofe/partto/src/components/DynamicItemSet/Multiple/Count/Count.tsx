import React from "react";

import { Progress } from "../Progress/Progress";
import { CountProps } from "./CountTypes";

export function Count({ on, total, title, onClick }: CountProps) {
  return (
    <span data-testid="Count">
      <Progress
        onClick={onClick}
        title={title}
        on={on}
        total={total}
        label={total.toString()}
      />
    </span>
  );
}
