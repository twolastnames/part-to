import React from "react";

import classes from "./ListItem.module.scss";
import { ListItemProps } from "./ListItemTypes";

export function ListItem({ precursor, description, trailer }: ListItemProps) {
  return (
    <div className={classes.listItem} data-testid="ListItem">
      {precursor && <div className={classes.precursor}>{precursor}</div>}
      <div className={classes.description}>{description}</div>
      {trailer && <div className={classes.trailer}>{trailer}</div>}
    </div>
  );
}
