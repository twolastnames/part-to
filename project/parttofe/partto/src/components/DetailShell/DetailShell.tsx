import React from "react";

import classes from "./DetailShell.module.scss";
import { DetailShellProps } from "./DetailShellTypes";
import { Body } from "../Body/Body";

export function DetailShell({ name, children }: DetailShellProps) {
  return (
    <div className={classes.detailShell} data-testid="DetailShell">
      <div className={classes.name}>{name}</div>
      <Body>{children}</Body>
    </div>
  );
}
