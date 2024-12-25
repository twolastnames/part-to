import React from "react";

import { ManageTasksProps, RunStateItemGetter } from "./ManageTasksTypes";
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
  getPrependedItems,
}: {
  typeKey: "duties" | "tasks";
  runState: RunStateId;
  emptyText: string;
  context: ContextDescription;
  getPrependedItems?: RunStateItemGetter;
}) {
  const response = useRunGet({ runState });
  return (
    <Spinner responses={[response]}>
      <ManageTasks
        context={context}
        emptyText={emptyText}
        tasks={response.data?.[typeKey] || []}
        runState={runState}
        getPrependedItems={getPrependedItems}
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
  getPrependedItems,
}: ManageTasksProps) {
  const navigate = useNavigate();
  const runStateData = useRunGet({ runState });

  const prepended =
    getPrependedItems && runStateData.data
      ? getPrependedItems(navigate, runStateData.data)
      : [];

  return (
    <DynamicItemSet
      context={context}
      items={(prepended.length > 0 ? [prepended[0]] : prepended).concat(
        getItems(navigate, runState, tasks),
      )}
      setOperations={[]}
      emptyPage={<EmptySimpleView content={emptyText} />}
    />
  );
}
