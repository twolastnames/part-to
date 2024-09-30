import React from "react";

import classes from "./ButtonSet.module.scss";
import { Operation } from "../DynamicItemSet";
import { Button, ButtonProps } from "../../Button/Button";

export interface ButtonSetProps {
  operations: Array<ButtonProps>;
}

export function ButtonSet(props: ButtonSetProps) {
  return (
    <div className={classes.buttonSet} data-testid="ButtonSet">
      {props.operations.map((operation: Operation) => (
        <Button {...operation} />
      ))}
    </div>
  );
}
