import React from "react";

import classes from "./AdjustableDigit.module.scss";
import { AdjustableDigitProps } from "./AdjustableDigitTypes";

export function AdjustableDigit({
  children,
  increment,
  decrement,
}: AdjustableDigitProps) {
  return (
    <span className={classes.adjustableDigit} data-testid="AdjustableDigit">
      {increment && (
        <div onClick={increment} className={classes.increment}>
          &gt;
        </div>
      )}
      {children}
      {decrement && (
        <div onClick={decrement} className={classes.decrement}>
          &gt;
        </div>
      )}
    </span>
  );
}
