import React from "react";

import classes from "./Layout.module.scss";
import {
  DynamicItemSet,
  DynamicItemSetProps,
} from "../DynamicItemSet/DynamicItemSet";

export interface LayoutProps {
  pair: [DynamicItemSetProps, DynamicItemSetProps];
}

export function Layout({ pair }: LayoutProps) {
  return (
    <div className={classes.layout} data-testid="Layout">
      {pair.map((set, index) => (
        <div className={classes.itemSet}>
          <DynamicItemSet key={index} {...set} />
        </div>
      ))}
    </div>
  );
}
