import React, { MutableRefObject } from "react";

import { RunStateId, TaskDefinitionId } from "../../api/sharedschemas";
import { DynamicItemSet } from "../DynamicItemSet/DynamicItemSet";
import { useRunGet } from "../../api/runget";
import { Spinner } from "../Spinner/Spinner";
import { DefinitionIdFromer } from "../PartTo/Definition/Definition";
import { Cancel } from "../Icon/Icon";
import { doRunvoidPost } from "../../api/runvoidpost";
import { useNavigate } from "react-router-dom";
import { getRoute } from "../../routes";

export interface ReviewStagedPartTosProps {
  taskDefinitions: Array<TaskDefinitionId>;
  runState: MutableRefObject<RunStateId>;
}

export function ReviewStagedPartTosIdFromer({
  runState,
}: {
  runState: MutableRefObject<RunStateId>;
}) {
  const response = useRunGet({ runState: runState.current });
  return (
    <Spinner responses={[response]}>
      <ReviewStagedPartTos
        runState={runState}
        taskDefinitions={response?.data?.staged || []}
      />
    </Spinner>
  );
}

function getItems(
  navigate: (arg: string) => void,
  runState: MutableRefObject<RunStateId>,
  taskDefinitions: Array<TaskDefinitionId>,
) {
  return taskDefinitions.map((taskDefinitionId: TaskDefinitionId) => ({
    key: taskDefinitionId,
    listView: <>{taskDefinitionId}</>,
    detailView: <DefinitionIdFromer task={taskDefinitionId} />,
    itemOperations: [
      {
        text: "Skip and Void",
        icon: Cancel,
        onClick: () => {
          doRunvoidPost({
            body: {
              runState: runState.current,
              definitions: [taskDefinitionId],
            },
            on200: ({ runState }) =>
              navigate(getRoute("StageMeal", { runState: runState })),
          });
        },
      },
    ],
  }));
}

export function ReviewStagedPartTos({
  taskDefinitions,
  runState,
}: ReviewStagedPartTosProps) {
  const navigate = useNavigate();
  const items = getItems(navigate, runState, taskDefinitions);
  return (
    <DynamicItemSet
      items={items}
      setOperations={[]}
      emptyPage={
        <>
          {[
            "Select recipes from the left with the arrow",
            "button to put a meal together.",
          ].join(" ")}
        </>
      }
    />
  );
}
