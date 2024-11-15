import React from "react";

import classes from "./EmptySimpleView.module.scss";
import { Empty, Icon } from "../../Icon/Icon";
import { EmptySimpleViewProps } from "./EmptySimpleViewTypes";
import { Size } from "../../Icon/IconTypes";

export function EmptySimpleView({ content }: EmptySimpleViewProps) {
  return (
    <div className={classes.emptySimpleView} data-testid="EmptySimpleView">
      <div className={classes.icon}>
        <Icon definition={Empty} size={Size.Large} />
      </div>
      <div className={classes.content}>{content}</div>
    </div>
  );
}
