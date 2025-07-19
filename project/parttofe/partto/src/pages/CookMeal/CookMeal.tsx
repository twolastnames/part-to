import React from "react";

import { Layout } from "../../components/Layout/Layout";
import { ManageTasksIdFromer } from "../../components/ManageTasks/ManageTasks";
import { LeftContext, RightContext } from "../../providers/DynamicItemSetPair";
import { getImminentItems } from "../../components/ManageTasks/Imminent/Imminent";
import {
  DutyClassNames,
  TaskClassNames,
} from "../../components/TaskDefinition/TaskDefinition";
import {
  Duty,
  Imminent,
  Task,
} from "../../components/TaskDefinition/Icon/Icon";
import { asItem } from "../../components/Overview/Overview";

type Entity = {
  name: string;
  side: string;
};

const getEmptyText = (target: Entity, other: Entity) =>
  [
    `No current ${target.name}. If any ${target.name} are left,`,
    `at least some the ${other.name}`,
    `on the ${other.side} pane need to be finished first.`,
  ].join(" ");

export function CookMeal() {
  return (
    <Layout
      pair={[
        <ManageTasksIdFromer
          definitionListSets={{
            imminent: Imminent,
            task: Task,
            duty: Duty,
          }}
          typeKey="duties"
          context={LeftContext}
          emptyText={getEmptyText(
            { name: "duties", side: "first" },
            { name: "tasks", side: "second" },
          )}
          getPrependedItems={getImminentItems}
          definitionClassNames={DutyClassNames}
        />,
        <ManageTasksIdFromer
          definitionListSets={{
            imminent: Imminent,
            task: Task,
            duty: Duty,
          }}
          context={RightContext}
          typeKey="tasks"
          emptyText={getEmptyText(
            { name: "tasks", side: "second" },
            { name: "duties", side: "first" },
          )}
          getPrependedItems={(navigate, runState, context, mapIndex) => [
            asItem({ runState: runState.runState }),
          ]}
          definitionClassNames={TaskClassNames}
        />,
      ]}
    />
  );
}
