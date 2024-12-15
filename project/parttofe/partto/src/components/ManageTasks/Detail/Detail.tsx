import React from "react";

import classes from "./Detail.module.scss";
import { DetailProps } from "./DetailTypes";
import { useTaskGet } from "../../../api/taskget";
import { useRunGet } from "../../../api/runget";
import { Spinner } from "../../Spinner/Spinner";
import { Timer } from "../../Timer/Timer";
import { useTaskdurationmetricGet } from "../../../api/taskdurationmetricget";
import { getDuration } from "../../../shared/duration";
import { useParttoGet } from "../../../api/parttoget";

export function Detail({ task, runState }: DetailProps) {
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
        <Timer
          start={
            runStateResponse.data?.startTimes.find(
              ({ task: taskId }) => taskId === task,
            )?.started
          }
          duration={metricResponse.data?.estimatedDuration || getDuration(0)}
        />
        <div className={classes.description}>
          {taskResponse.data?.description}
        </div>
        <ul>
          {taskResponse.data?.ingredients.map((ingredient) => <li>{ingredient}</li>)}
        </ul>
        {partToResponse.data && (
          <div>For Recipe: {partToResponse.data?.name}</div>
        )}
      </div>
    </Spinner>
  );
}
