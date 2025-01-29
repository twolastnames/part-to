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
import { ClassNames as DefinitionClassNames } from "../TaskDefinition/TaskDefinitionTypes";
import { RunGet200Body } from "../../api/runget";
import { ListItem } from "../TaskDefinition/ListItem/ListItem";
import { IconClassSets } from "../TaskDefinition/ListItem/ListItemTypes";

export function ManageTasksIdFromer({
  typeKey,
  emptyText,
  definitionListSets,
  context,
  getPrependedItems,
  definitionClassNames,
}: {
  typeKey: "duties" | "tasks";
  emptyText: string;
  definitionListSets: IconClassSets;
  context: ContextDescription;
  getPrependedItems?: RunStateItemGetter;
  definitionClassNames: DefinitionClassNames;
}) {
  const response = useRunState();
  const tasks = (response?.data?.["started"] || []).filter((key) =>
    (response.data?.[typeKey] || []).includes(key),
  );
  return (
    <Spinner responses={[response]}>
      <ManageTasks
        definitionListSets={definitionListSets}
        context={context}
        emptyText={emptyText}
        tasks={tasks}
        getPrependedItems={getPrependedItems}
        definitionClassNames={definitionClassNames}
      />
    </Spinner>
  );
}

function getItems(
  definitionClassNames: DefinitionClassNames,
  definitionListSets: IconClassSets,
  navigate: (arg: string) => void,
  runState: RunStateId,
  tasks: Array<TaskDefinitionId>,
  context: ContextDescription,
  offset: number,
) {
  return tasks.map((taskDefinitionId: TaskDefinitionId, index: number) => ({
    key: taskDefinitionId,
    listView: (
      <ListItem
        iconClassSets={definitionListSets}
        runState={runState}
        task={taskDefinitionId}
      />
    ),
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

function isComplete(runState?: RunGet200Body) {
  return (
    runState &&
    runState.completed.length &&
    !runState.staged.length &&
    !runState.started.length
  );
}

const completedText = "Done Yo!";

export function ManageTasks({
  context,
  tasks,
  emptyText,
  getPrependedItems,
  definitionClassNames,
  definitionListSets,
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
            definitionListSets,
            navigate,
            runStateData?.data?.runState as RunStateId,
            tasks,
            context,
            prepended.length ? 1 : 0,
          ),
        )}
        setOperations={[]}
        emptyPage={
          <EmptySimpleView
            content={isComplete(runStateData.data) ? completedText : emptyText}
          />
        }
      />
    </Spinner>
  );
}
