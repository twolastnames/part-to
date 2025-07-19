import React from "react";

import classes from "./Title.module.scss";
import { TitleProps } from "./TitleTypes";
import { Icon } from "../Icon/Icon";
import { Size } from "../Icon/IconTypes";

export function Title({ icon, children }: TitleProps) {
  return (
    <div className={classes.title} data-testid="Title">
      <div className={classes.icon}>
        <Icon definition={icon} size={Size.Small} />
      </div>
      <div className={classes.text}>{children}</div>
    </div>
  );
}
