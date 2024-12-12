import React from "react";

import classes from "./List.module.scss";
import { ImminentProps } from "../ImminentTypes";
import { useTaskGet } from "../../../../api/taskget";
import { Spinner } from "../../../Spinner/Spinner";
import { TimerString } from "../TimerString/TimerString";

export function List({ timestamp, till, duty }: ImminentProps) {
  const taskResponse = useTaskGet({ task: duty });
  return (
    <Spinner responses={[taskResponse]}>
      <div className={classes.list} data-testid="List">
        "Duty Start Time:"
        <TimerString started={timestamp} duration={till} />
        {`to "${taskResponse.data?.description}"`}
      </div>
    </Spinner>
  );
}
