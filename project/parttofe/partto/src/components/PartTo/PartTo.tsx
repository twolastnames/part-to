import React, { ReactNode } from "react";

import classes from "./PartTo.module.scss";
import { PartToId, TaskDefinitionId } from "../../api/sharedschemas";
import { useParttoGet } from "../../api/parttoget";
import { Duration, Stage } from "../../api/helpers";
import { DefinitionIdFromer } from "./Definition/Definition";

export interface PartToProps {
  name: string;
  workDuration?: Duration;
  clockDuration?: Duration;
  tasks: Array<ReactNode>;
}

export function PartToIdFromer({ partTo }: { partTo: PartToId }) {
  const response = useParttoGet({ partTo });
  if (response.stage !== Stage.Ok || !response?.data) {
    return <></>;
  }
  const { name, workDuration, clockDuration, tasks } = response.data;

  return (
    <PartTo
      key={partTo}
      name={name}
      workDuration={workDuration}
      clockDuration={clockDuration}
      tasks={tasks.map((task: TaskDefinitionId) => (
        <DefinitionIdFromer key={task} task={task} />
      ))}
    />
  );
}

export function PartTo({
  name,
  workDuration,
  clockDuration,
  tasks,
}: PartToProps) {
  return (
    <div className={classes.partTo} data-testid="PartTo">
      <div className={classes.name}>{name}</div>
      <div className={classes.workDuration}>
        {workDuration?.toMilliseconds() || ""}
      </div>
      <div className={classes.clockDuration}>
        {clockDuration?.toMilliseconds() || ""}
      </div>
      <div className={classes.tasks}>
        {tasks.map((task) => (
          <div key={Math.random()} className={classes.task}>
            {task}
          </div>
        ))}
      </div>
    </div>
  );
}
