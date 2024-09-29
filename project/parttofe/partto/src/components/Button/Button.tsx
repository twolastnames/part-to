import React, { PropsWithChildren } from "react";
import {
  Button as MantineButton,
} from "@mantine/core";

import classes from "./Button.module.scss";

export interface ButtonProps extends PropsWithChildren {onClick: () => void}

console.log({classes})

export const Button = (props: ButtonProps) => (
  <MantineButton data-testid="Button" classNames={classes.button} {...props} />
);
