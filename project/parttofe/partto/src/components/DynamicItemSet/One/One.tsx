import React from "react";

import classes from "./One.module.scss";
import { ButtonSet } from "../ButtonSet/ButtonSet";
import { OneProps } from "./OneTypes";

export function One({ item }: OneProps) {
  return (
    <div className={classes.one} data-testid="One">
      <div className={classes.content}>{item.detailView}</div>
      <ButtonSet operations={item.itemOperations} />
    </div>
  );
}
