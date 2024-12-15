import React from "react";

import classes from "./Note.module.scss";
import { NoteProps } from "./NoteTypes";
export function Note({ heading, detail, onClick }: NoteProps) {
  return (
    <div
      className={[classes.note, onClick ? classes.clickable : ""].join(" ")}
      onClick={() => onClick && onClick()}
      data-testid="Note"
    >
      <div className={classes.heading}>{heading}</div>
      <div className={classes.detail}>{detail}</div>
    </div>
  );
}
