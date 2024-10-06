import React from "react";
import { ActionIcon as MantineButton, Tooltip } from "@mantine/core";

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
      <div onClick={onClick} className={classes.container}>
        <MantineButton
          data-testid="Button"
          aria-label={text}
          className={classes.button}
        >
          <Icon definition={icon} size={IconSize.Small} />
        </MantineButton>
      </div>
    </Tooltip>
  </>
);
