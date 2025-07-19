import React from "react";

import classes from "./List.module.scss";
import { useSingleOfPair } from "../../../../providers/DynamicItemSetPair";
import { ListProps } from "./ListTypes";

export function List({ items, context, onSelectionChanged }: ListProps) {
  const { setSelected } = useSingleOfPair(context);
  return (
    <div className={classes.list} data-testid="List" style={{ height: "100%" }}>
      {items.map(({ listView }, index: number) => (
        <div className={classes.row}>
          <div
            onClick={() => {
              setSelected(index);
              onSelectionChanged();
            }}
            className={classes.item}
          >
            {listView}
          </div>
        </div>
      ))}
    </div>
  );
}
