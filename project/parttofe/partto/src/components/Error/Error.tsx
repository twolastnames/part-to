import React from "react";

import classes from "./Error.module.scss";
import { ErrorProps } from "./ErrorTypes";

export function Error({ code }: ErrorProps) {
  return (
    <div className={classes.error} data-testid="Error">
      <div className={classes.code}>{code}</div>
      <div className={classes.description}>
        This is bad. There is nothing here. You and your family could starve if
        you expected to cook dinner here. They could be saved by navigating to
        some place more useful in the site navigation menu.
      </div>
    </div>
  );
}
