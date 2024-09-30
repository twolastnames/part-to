import React from "react";
import { Button as MantineButton, Tooltip } from "@mantine/core";

import classes from "./Button.module.scss";
import { IconType, Icon, Size as IconSize } from "../Icon/Icon";

export interface ButtonProps {
  text: string;
  icon: IconType;
  onClick: () => void;
}

export const Button = ({ onClick, icon, text }: ButtonProps) => (
  <>
    <Tooltip label={text} data-testid="Button">
      <div className={classes.container}>
        <MantineButton
          data-testid="Button"
          onClick={onClick}
          className={classes.button}
        />
        <span className={classes.icon}>
          <Icon onClick={onClick} definition={icon} size={IconSize.Small} />
        </span>
      </div>
    </Tooltip>
  </>
);
