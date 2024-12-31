import React, { PropsWithChildren } from "react";

import classes from "./Flasher.module.scss";

export function Flasher({ children }: PropsWithChildren) {
  return (
    <span className={classes.flasher} data-testid="Flasher">
      {children}
    </span>
  );
}
