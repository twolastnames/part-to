import React, { useEffect, useState } from "react";
import { ActionIcon as MantineButton, Tooltip } from "@mantine/core";

import classes from "./Button.module.scss";
import { Icon } from "../Icon/Icon";
import { ButtonProps } from "./ButtonTypes";
import { Size } from "../Icon/IconTypes";

export const Button = ({ onClick, icon, text }: ButtonProps) => {
  return (
    <>
      <Tooltip label={text} data-testid="Button">
        <div onClick={onClick} className={classes.container}>
          <MantineButton
            data-testid="Button"
            aria-label={text}
            className={classes.button}
          >
            <Icon definition={icon} size={Size.Small} />
          </MantineButton>
        </div>
      </Tooltip>
    </>
  );
};
