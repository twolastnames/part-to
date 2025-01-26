import React from "react";

import classes from "./DetailShell.module.scss";
import { DetailShellProps } from "./DetailShellTypes";

export function DetailShell({ name, children }: DetailShellProps) {
  return (
    <div className={classes.detailShell} data-testid="DetailShell">
      <div className={classes.name}>{name}</div>
      <div className={classes.children}>{children}</div>
    </div>
  );
}
