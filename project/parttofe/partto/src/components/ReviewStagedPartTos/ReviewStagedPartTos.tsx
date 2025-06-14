import React from "react";

import { RunStateId, TaskDefinitionId } from "../../api/sharedschemas";
import { DynamicItemSet } from "../DynamicItemSet/DynamicItemSet";
import { Spinner } from "../Spinner/Spinner";
import { Cancel, Oven } from "../Icon/Icon";
import { doRunvoidPost } from "../../api/runvoidpost";
import { useNavigate } from "react-router-dom";
import { getRoute } from "../../routes";
import { doRunstartPost } from "../../api/runstartpost";
import { ReviewStagedPartTosProps } from "./ReviewStagedPartTosTypes";
import { LeftContext, RightContext } from "../../providers/DynamicItemSetPair";
import { useRunState } from "../../hooks/runState";
import {
  StagedClassNames,
  TaskDefinition,
} from "../TaskDefinition/TaskDefinition";
import { ListItem } from "../TaskDefinition/ListItem/ListItem";
import { Duty, Task } from "../TaskDefinition/Icon/Icon";
import { asItem } from "../Overview/Overview";

export function ReviewStagedPartTosIdFromer() {
  const response = useRunState();
  return (
    <Spinner responses={[response]}>
      <ReviewStagedPartTos taskDefinitions={response?.data?.staged || []} />
    </Spinner>
  );
}

function getItems(
  navigate: (arg: string) => void,
  runState: RunStateId,
  taskDefinitions: Array<TaskDefinitionId>,
  prependedOffset: number,
) {
  return taskDefinitions.map(
    (taskDefinitionId: TaskDefinitionId, index: number) => ({
      key: taskDefinitionId,
      listView: (
        <ListItem
          iconClassSets={{
            imminent: Duty,
            task: Task,
            duty: Duty,
          }}
          runState={runState}
          task={taskDefinitionId}
        />
      ),
      detailView: (
        <TaskDefinition
          task={taskDefinitionId}
          runState={runState}
          locatable={{
            onLocate: (setter) => () => {
              setter(index + prependedOffset);
            },
            context: RightContext,
          }}
          classNames={StagedClassNames}
        />
      ),
      itemOperations: [
        {
          text: "Skip and Void",
          icon: Cancel,
          onClick: () => {
            doRunvoidPost({
              body: {
                runState: runState,
                definitions: [taskDefinitionId],
              },
              on200: ({ runState }) => {
                navigate(getRoute("StageMeal", { runState: runState }));
              },
            });
          },
        },
      ],
    }),
  );
}

export function ReviewStagedPartTos({
  taskDefinitions,
}: ReviewStagedPartTosProps) {
  const navigate = useNavigate();
  const response = useRunState();
  const runState = response?.data?.runState as RunStateId;
  const prepended = runState ? [asItem({ runState })] : [];
  const items = runState
    ? [
        ...prepended,
        ...getItems(navigate, runState, taskDefinitions, prepended.length),
      ]
    : [];
  return (
    <Spinner responses={[response]}>
      <DynamicItemSet
        items={items}
        context={RightContext}
        pausedByDefault={true}
        setOperations={[
          {
            text: "Start Cooking",
            icon: Oven,
            onClick: () => {
              doRunstartPost({
                body: { runState: response.data?.runState },
                on200: ({ runState }) => {
                  LeftContext.setCount(0);
                  LeftContext.setSettingKey("duties");
                  RightContext.setCount(0);
                  RightContext.setSettingKey("tasks");
                  navigate(getRoute("CookMeal", { runState }));
                },
              });
            },
          },
        ]}
        emptyPage={
          <>
            {[
              "Select recipes from the first pane with the plus",
              "and add tasks for meal a meal to the second",
              "pane. When all your meal tasks are in the second pane,",
              "click the oven that will appear to start cooking.",
            ].join(" ")}
          </>
        }
      />
    </Spinner>
  );
}
