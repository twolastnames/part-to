import React from "react";

import classes from "./Detail.module.scss";
import { DetailProps } from "./DetailTypes";
import { useTaskGet } from "../../../api/taskget";
import { useRunGet } from "../../../api/runget";
import { Spinner } from "../../Spinner/Spinner";
import { useTaskdurationmetricGet } from "../../../api/taskdurationmetricget";
import { useParttoGet } from "../../../api/parttoget";
import { useTimerProvider } from "../../../providers/Timer";

export function Detail({ task, runState }: DetailProps) {
  const timer = useTimerProvider({ task });
  const taskResponse = useTaskGet({ task });
  const partToResponse = useParttoGet(
    { partTo: taskResponse?.data?.partTo || "" },
    { shouldSkip: () => !taskResponse.data },
  );
  const runStateResponse = useRunGet({ runState });
  const metricResponse = useTaskdurationmetricGet({ task });
  return (
    <Spinner responses={[taskResponse, runStateResponse, metricResponse]}>
      <div className={classes.detail} data-testid="Detail">
        {timer}
        <div className={classes.description}>
          {taskResponse.data?.description}
        </div>
        <ul>
          {taskResponse.data?.ingredients.map((ingredient) => (
            <li>{ingredient}</li>
          ))}
        </ul>
        {partToResponse.data && (
          <div>For Recipe: {partToResponse.data?.name}</div>
        )}
      </div>
    </Spinner>
  );
}
