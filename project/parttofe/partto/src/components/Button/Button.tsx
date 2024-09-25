import React, { PropsWithChildren } from "react";
import {
  Button as MantineButton,
  ButtonProps as MantineButtonProps,
} from "@mantine/core";

import classes from "./Button.module.css";

export interface ButtonProps extends PropsWithChildren {onClick: () => void}

console.log({classes})

export const Button = (props: ButtonProps) => (
  <MantineButton data-testid="Button" className={classes.buttonBase} {...props} />
);
