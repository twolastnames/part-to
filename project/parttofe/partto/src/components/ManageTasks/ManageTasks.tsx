import React from "react";

import { ManageTasksProps, RunStateItemGetter } from "./ManageTasksTypes";
import { RunStateId, TaskDefinitionId } from "../../api/sharedschemas";
import { Spinner } from "../Spinner/Spinner";
import { DynamicItemSet } from "../DynamicItemSet/DynamicItemSet";
import { ContextDescription } from "../../providers/DynamicItemSetPair";
import { EmptySimpleView } from "../DynamicItemSet/EmptySimpleView/EmptySimpleView";
import { useNavigate } from "react-router-dom";
import { doRunvoidPost } from "../../api/runvoidpost";
import { getRoute } from "../../routes";
import { Cancel, Check } from "../Icon/Icon";
import { doRuncompletePost } from "../../api/runcompletepost";
import { TaskDefinition } from "../TaskDefinition/TaskDefinition";
import { useRunState } from "../../hooks/runState";
import { ClassNames } from "../TaskDefinition/TaskDefinitionTypes";

export function ManageTasksIdFromer({
  typeKey,
  emptyText,
  context,
  getPrependedItems,
  definitionClassNames,
}: {
  typeKey: "duties" | "tasks";
  emptyText: string;
  context: ContextDescription;
  getPrependedItems?: RunStateItemGetter;
  definitionClassNames: ClassNames;
}) {
  const response = useRunState();
  return (
    <Spinner responses={[response]}>
      <ManageTasks
        context={context}
        emptyText={emptyText}
        tasks={response.data?.[typeKey] || []}
        getPrependedItems={getPrependedItems}
        definitionClassNames={definitionClassNames}
      />
    </Spinner>
  );
}

function getItems(
  definitionClassNames: ClassNames,
  navigate: (arg: string) => void,
  runState: RunStateId,
  tasks: Array<TaskDefinitionId>,
  context: ContextDescription,
  offset: number,
) {
  return tasks.map((taskDefinitionId: TaskDefinitionId, index: number) => ({
    key: taskDefinitionId,
    listView: <>{taskDefinitionId}</>,
    detailView: (
      <TaskDefinition
        locatable={{
          context,
          onLocate: (setter: (value: number) => void) => () => {
            setter(index + offset);
          },
        }}
        task={taskDefinitionId}
        runState={runState}
        classNames={definitionClassNames}
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
  emptyText,
  getPrependedItems,
  definitionClassNames,
}: ManageTasksProps) {
  const navigate = useNavigate();
  const runStateData = useRunState();

  const prepended =
    getPrependedItems && runStateData.data
      ? getPrependedItems(navigate, runStateData.data, context, (ignored) => 0)
      : [];

  return (
    <Spinner responses={[runStateData]}>
      <DynamicItemSet
        context={context}
        items={(prepended.length > 0 ? [prepended[0]] : prepended).concat(
          getItems(
            definitionClassNames,
            navigate,
            runStateData?.data?.runState as RunStateId,
            tasks,
            context,
            prepended.length ? 1 : 0,
          ),
        )}
        setOperations={[]}
        emptyPage={<EmptySimpleView content={emptyText} />}
      />
    </Spinner>
  );
}
