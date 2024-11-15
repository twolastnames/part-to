import React from "react";

import classes from "./Layout.module.scss";
import { LayoutProps } from "./LayoutTypes";

export function Layout({ pair }: LayoutProps) {
  return (
    <div className={classes.layout} data-testid="Layout">
      {pair.map((set) => (
        <div key={Math.random()} className={classes.itemSet}>
          {set}
        </div>
      ))}
    </div>
  );
}
