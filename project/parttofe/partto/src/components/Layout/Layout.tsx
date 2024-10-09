import React, { ReactNode } from "react";

import classes from "./Layout.module.scss";
import { NavigationBar } from "./NavigationBar/NavigationBar";
import {
  DynamicItemSet,
  DynamicItemSetProps,
} from "../DynamicItemSet/DynamicItemSet";

export interface LayoutProps {
  pair: [DynamicItemSetProps, DynamicItemSetProps];
  extra: ReactNode;
}

export function Layout({ pair, extra }: LayoutProps) {
  return (
    <div className={classes.layout} data-testid="Layout">
      <NavigationBar extra={extra} />
      {pair.map((set, index) => (
        <div className={classes.itemSet}>
          <DynamicItemSet key={index} {...set} />
        </div>
      ))}
    </div>
  );
}
