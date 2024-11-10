import React from "react";

import { Progress } from "../Progress/Progress";

export interface CountProps {
  on: number;
  total: number;
  title: string;
  onClick: () => void;
}

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
