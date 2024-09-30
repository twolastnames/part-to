import React from "react";

import classes from "./DynamicItemSet.module.scss";
import { IconType } from "../Icon/Icon";
import { Empty } from "./Empty/Empty";
import { One } from "./One/One";
import { Multiple } from "./Multiple/Multiple";
import { ButtonSet } from "./ButtonSet/ButtonSet";

export interface Operation {
  text: string;
  icon: IconType;
  onClick: () => void;
}

export interface Item {
  listView: React.ReactElement;
  detailView: React.ReactElement;
  itemOperations: Array<Operation>;
}

export interface DynamicItemSetProps {
  items: Array<Item>;
  setOperations: Array<Operation>;
  emptyPage: React.ReactElement;
}

export function DynamicItemSet({
  setOperations,
  items,
  emptyPage,
}: DynamicItemSetProps) {
  return (
    <div className={classes.dynamicItemSet} data-testid="DynamicItemSet">
      <ButtonSet operations={setOperations} />
      {items.length === 0 ? (
        <Empty content={emptyPage} />
      ) : items.length === 1 ? (
        <One item={items[0]} />
      ) : (
        <Multiple items={items} />
      )}
    </div>
  );
}
