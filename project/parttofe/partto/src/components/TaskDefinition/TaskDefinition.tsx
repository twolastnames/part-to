import React from "react";
import classes from "./TaskDefinition.module.scss";
import { ClassNames, TaskDefinitionProps } from "./TaskDefinitionTypes";
import { useTaskGet } from "../../api/taskget";
import { useRunGet } from "../../api/runget";
import { Spinner } from "../Spinner/Spinner";
import { useParttoGet } from "../../api/parttoget";
import { useTimerProvider } from "../../providers/Timer";
import { useSingleOfPair } from "../../providers/DynamicItemSetPair";
import {
  Definition,
  DefinitionListed,
} from "../DefinitionListed/DefinitionListed";
import { Body } from "../Body/Body";
import { Title } from "../Title/Title";
import { Duty, Icon, Imminent, Recipe, Task } from "../Icon/Icon";
import { ListItem } from "../ListItem/ListItem";

export const TaskClassNames: ClassNames = {
  layout: classes.task,
  timer: classes.normalTimer,
  upcomingTitle: classes.hidden,
  upcomingDescription: classes.hidden,
};

export const DutyClassNames: ClassNames = {
  layout: classes.duty,
  timer: classes.normalTimer,
  upcomingTitle: classes.hidden,
  upcomingDescription: classes.hidden,
};

export const ImminentClassNames: ClassNames = {
  layout: classes.imminent,
  timer: classes.upcomingTimer,
  upcomingTitle: classes.upcomingTitle,
  upcomingDescription: classes.upcomingDescription,
};

export const StagedClassNames: ClassNames = {
  layout: classes.staged,
  timer: classes.hidden,
  upcomingTitle: classes.hidden,
  upcomingDescription: classes.hidden,
};

export function TaskDefinition({
  task,
  runState,
  locatable,
  classNames,
}: TaskDefinitionProps) {
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

  const imminent = runStateResponse?.data?.timers.imminent.some(
    (imminent) => task === imminent.task,
  );

  return (
    <Spinner responses={[taskResponse, runStateResponse]}>
      <div className={classes.taskDefinition} data-testid="TaskDefinition">
        <div className={classNames.layout}>
          <h3 className={classNames.upcomingTitle}>Upcoming:</h3>
          <div className={classNames.upcomingDescription}>
            You don't need to do anything about this yet. It's just warning of
            what is coming. Start at your own risk of having cold food at the
            end. We've seen from Hollywood films that time travel can go bad.
          </div>

          <div className={classNames.timer}>{timer}</div>
          <div className={classes.description}>
            <ListItem
              precursor={
                <Icon
                  definition={
                    imminent
                      ? Imminent
                      : runStateResponse.data?.duties.includes(task)
                        ? Duty
                        : Task
                  }
                />
              }
              description={taskResponse.data?.description}
            />
          </div>
        </div>
        <Body>
          <DefinitionListed summary="Ingredients">
            <Definition definitionKey="ingredients" id={task} />
          </DefinitionListed>
          <DefinitionListed summary="Tools">
            <Definition definitionKey="tools" id={task} />
          </DefinitionListed>
          <Title icon={Recipe}>{partToResponse.data?.name}</Title>
        </Body>
      </div>
    </Spinner>
  );
}
