import React from "react";

import classes from "./One.module.scss";
import { Item } from "../DynamicItemSet";
import { ButtonSet } from "../ButtonSet/ButtonSet";

export interface OneProps {
  item: Item;
}

export function One({ item }: OneProps) {
  return (
    <div className={classes.one} data-testid="One">
      <div className={classes.content}>{item.detailView}</div>
      <ButtonSet operations={item.itemOperations} />
    </div>
  );
}
