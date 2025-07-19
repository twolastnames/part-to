import React from "react";

import classes from "./DynamicItemSet.module.scss";
import { Empty } from "./Empty/Empty";
import { One } from "./One/One";
import { Multiple } from "./Multiple/Multiple";
import { ButtonSet } from "./ButtonSet/ButtonSet";
import { DynamicItemSetProps } from "./DynamicItemSetTypes";

export function DynamicItemSet({
  setOperations,
  items,
  emptyPage,
  pausedByDefault,
  context,
}: DynamicItemSetProps) {
  context.setCount(items.length);
  return (
    <div className={classes.dynamicItemSet} data-testid="DynamicItemSet">
      <ButtonSet operations={setOperations} />
      {items.length === 0 ? (
        <Empty content={emptyPage} />
      ) : items.length === 1 ? (
        <One item={items[0]} />
      ) : (
        <Multiple
          pausedByDefault={pausedByDefault}
          context={context}
          items={items}
        />
      )}
    </div>
  );
}
