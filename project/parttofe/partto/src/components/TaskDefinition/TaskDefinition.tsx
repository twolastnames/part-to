import React from "react";
import classes from "./TaskDefinition.module.scss";
import { DetailProps } from "./TaskDefinitionTypes";
import { useTaskGet } from "../../api/taskget";
import { useRunGet } from "../../api/runget";
import { Spinner } from "../Spinner/Spinner";
import { useParttoGet } from "../../api/parttoget";
import { useTimerProvider } from "../../providers/Timer";
import { useSingleOfPair } from "../../providers/DynamicItemSetPair";

export function TaskDefinition({ task, runState, locatable }: DetailProps) {
  const { setSelected } = useSingleOfPair(locatable.context);
  const timer = useTimerProvider({
    task,
    ...(locatable ? { onLocate: locatable.onLocate(setSelected) } : {}),
  });
  const taskResponse = useTaskGet({ task });
  const partToResponse = useParttoGet(
    { partTo: taskResponse?.data?.partTo || "" },
    { shouldSkip: () => !taskResponse.data },
  );
  const runStateResponse = useRunGet({ runState });
  return (
    <Spinner responses={[taskResponse, runStateResponse]}>
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
