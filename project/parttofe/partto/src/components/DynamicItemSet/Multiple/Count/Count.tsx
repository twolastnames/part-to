import React from "react";

import { Progress } from "../Progress/Progress";

export interface CountProps {
  on: number;
  total: number;
}

export function Count({ on, total }: CountProps) {
  return (
    <span data-testid="Count">
      <Progress on={on} total={total} label={total.toString()} />
    </span>
  );
}
