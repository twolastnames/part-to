import React from "react";

import classes from "./Empty.module.scss";
import { EmptyProps } from "./EmptyTypes";

export function Empty({ content }: EmptyProps) {
  return (
    <div className={classes.empty} data-testid="Empty">
      {content}
    </div>
  );
}
