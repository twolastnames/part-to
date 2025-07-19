import React, { PropsWithChildren } from "react";

import classes from "./Body.module.scss";

export function Body({ children }: PropsWithChildren) {
  return (
    <div className={classes.body} data-testid="Body">
      {children}
    </div>
  );
}
