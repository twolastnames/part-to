import React, { ReactNode } from "react";

import classes from "./EmptySimpleView.module.scss";
import { Empty, Icon } from "../../Icon/Icon";
import { Size } from "../../Icon/Icon";

export interface EmptySimpleViewProps {
  content: ReactNode;
}

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
