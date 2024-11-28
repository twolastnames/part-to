import React from "react";

import classes from "./ManageTasks.module.scss";
import { ManageTasksProps } from "./ManageTasksTypes";
import { RunStateId, TaskDefinitionId } from "../../api/sharedschemas";
import { useRunGet } from "../../api/runget";
import { Spinner } from "../Spinner/Spinner";
import { DynamicItemSet } from "../DynamicItemSet/DynamicItemSet";
import { ContextDescription } from "../../providers/DynamicItemSetPair";
import { EmptySimpleView } from "../DynamicItemSet/EmptySimpleView/EmptySimpleView";
import { useNavigate } from "react-router-dom";
import { doRunvoidPost } from "../../api/runvoidpost";
import { getRoute } from "../../routes";
import { Cancel, Check } from "../Icon/Icon";
import { doRuncompletePost } from "../../api/runcompletepost";
import { Detail } from "./Detail/Detail";

export function ManageTasksIdFromer({
  runState,
  typeKey,
  emptyText,
  context,
}: {
  typeKey: "duties" | "tasks";
  runState: RunStateId;
  emptyText: string;
  context: ContextDescription;
}) {
  const response = useRunGet({ runState });
  return (
    <Spinner responses={[response]}>
      <ManageTasks
        context={context}
        emptyText={emptyText}
        tasks={response.data?.[typeKey] || []}
        runState={runState}
      />
    </Spinner>
  );
}

function getItems(
  navigate: (arg: string) => void,
  runState: RunStateId,
  tasks: Array<TaskDefinitionId>,
) {
  return tasks.map((taskDefinitionId: TaskDefinitionId) => ({
    key: taskDefinitionId,
    listView: <>{taskDefinitionId}</>,
    detailView: <Detail task={taskDefinitionId} runState={runState} />,
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
            on200: ({ runState }) =>
              navigate(getRoute("CookMeal", { runState })),
          });
        },
      },
      {
        text: "Complete",
        icon: Check,
        onClick: () => {
          doRuncompletePost({
            body: {
              runState: runState,
              definitions: [taskDefinitionId],
            },
            on200: ({ runState }) =>
              navigate(getRoute("CookMeal", { runState })),
          });
        },
      },
    ],
  }));
}

export function ManageTasks({
  context,
  tasks,
  runState,
  emptyText,
}: ManageTasksProps) {
  const navigate = useNavigate();
  return (
    <div className={classes.manageTasks} data-testid="ManageTasks">
      <DynamicItemSet
        context={context}
        items={getItems(navigate, runState, tasks)}
        setOperations={[]}
        emptyPage={<EmptySimpleView content={emptyText} />}
      />
    </div>
  );
}
