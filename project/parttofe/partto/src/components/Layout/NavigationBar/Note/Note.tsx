import React from "react";

import classes from "./Note.module.scss";
import { NoteProps } from "./NoteTypes";
export function Note({ heading, detail }: NoteProps) {
  return (
    <div className={classes.note} data-testid="Note">
      <div className={classes.heading}>{heading}</div>
      <div className={classes.detail}>{detail}</div>
    </div>
  );
}
