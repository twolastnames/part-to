import React from "react";

import classes from "./Empty.module.scss";

export interface EmptyProps {
  content: React.ReactElement;
}

export function Empty({ content }: EmptyProps) {
  return (
    <div className={classes.empty} data-testid="Empty">
      {content}
    </div>
  );
}
