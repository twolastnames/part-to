import React from "react";

import classes from "./Detail.module.scss";
import { ImminentProps } from "../ImminentTypes";
import { useTaskGet } from "../../../../api/taskget";
import { Spinner } from "../../../Spinner/Spinner";
import { TimerString } from "../TimerString/TimerString";

export function Detail({ timestamp, till, duty }: ImminentProps) {
  const taskResponse = useTaskGet({ task: duty });
  return (
    <Spinner responses={[taskResponse]}>
      <div className={classes.list} data-testid="Detail">
        {`Duty Start Time: `}
        <TimerString started={timestamp} duration={till} />
        {` to "${taskResponse.data?.description}"`}
      </div>
    </Spinner>
  );
}
