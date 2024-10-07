import React, { ReactNode } from "react";

import classes from "./Note.module.scss";

export interface NoteProps {
  heading: ReactNode;
  detail: ReactNode;
}

export function Note({ heading, detail }: NoteProps) {
  return (
    <div className={classes.note} data-testid="Note">
      <div className={classes.heading}>{heading}</div>
      <div className={classes.detail}>{detail}</div>
    </div>
  );
}
