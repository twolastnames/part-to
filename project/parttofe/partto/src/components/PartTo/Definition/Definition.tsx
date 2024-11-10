import React from "react";

import classes from "./Definition.module.scss";
import { TaskDefinitionId } from "../../../api/sharedschemas";
import { useTaskGet } from "../../../api/taskget";
import { Stage } from "../../../api/helpers";

export interface DefinitionProps {
  description: string;
  duration: string;
}

export function DefinitionIdFromer({ task }: { task: TaskDefinitionId }) {
  const response = useTaskGet({ task });
  if (response.stage !== Stage.Ok || !response?.data) {
    return <></>;
  }
  const { description, duration } = response.data;
  return (
    <Definition
      key={task}
      description={description}
      duration={duration.toMilliseconds().toString() || ""}
    />
  );
}

export function Definition({ description, duration }: DefinitionProps) {
  return (
    <div className={classes.definition} data-testid="Definition">
      <div className={classes.description}>{description}</div>
      <div className={classes.duration}>{duration}</div>
    </div>
  );
}
