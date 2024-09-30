import React, { PropsWithChildren } from "react";
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
      <span>
        <MantineButton
          data-testid="Button"
          onClick={onClick}
          classNames={classes}
        />
        <Icon onClick={onClick} definition={icon} size={IconSize.Small} />
      </span>
    </Tooltip>
  </>
);
