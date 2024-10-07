import React from "react";

import classes from "./Layout.module.scss";
import { NavigationBar } from "./NavigationBar/NavigationBar";
import {
  DynamicItemSet,
  DynamicItemSetProps,
} from "../DynamicItemSet/DynamicItemSet";
import { NoteProps } from "./NavigationBar/Note/Note";

export interface LayoutProps {
  setPair: [DynamicItemSetProps, DynamicItemSetProps];
  notes: Array<NoteProps>;
}

export function Layout({ setPair, notes }: LayoutProps) {
  return (
    <div className={classes.layout} data-testid="Layout">
      <NavigationBar notes={notes} />
      {setPair.map((set) => (
        <div className={classes.itemSet}>
          <DynamicItemSet {...set} />
        </div>
      ))}
    </div>
  );
}
