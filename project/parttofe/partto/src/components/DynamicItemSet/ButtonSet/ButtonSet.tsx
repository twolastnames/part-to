import React from "react";

import classes from "./ButtonSet.module.scss";
import { Button } from "../../Button/Button";
import { ButtonSetProps } from "./ButtonSetTypes";
import { Operation } from "../DynamicItemSetTypes";

export function ButtonSet(props: ButtonSetProps) {
  return (
    <div className={classes.buttonSet} data-testid="ButtonSet">
      {props.operations.map((operation: Operation, index) => (
        <Button key={index} {...operation} />
      ))}
    </div>
  );
}
