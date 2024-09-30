import React from "react";

import classes from "./Multiple.module.scss";
import { Item } from "../DynamicItemSet";

export interface MultipleProps {
  items: Array<Item>;
}

export function Multiple({ items }: MultipleProps) {
  return (
    <div className={classes.multiple} data-testid="Multiple">
      WIP
    </div>
  );
}
