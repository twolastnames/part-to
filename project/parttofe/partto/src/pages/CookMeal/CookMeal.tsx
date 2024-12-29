import React from "react";

import { Layout } from "../../components/Layout/Layout";
import { ManageTasksIdFromer } from "../../components/ManageTasks/ManageTasks";
import { LeftContext, RightContext } from "../../providers/DynamicItemSetPair";
import { getImminentItems } from "../../components/ManageTasks/Imminent/Imminent";

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
          typeKey="duties"
          context={LeftContext}
          emptyText={getEmptyText(
            { name: "duties", side: "first" },
            { name: "tasks", side: "second" },
          )}
          getPrependedItems={getImminentItems}
        />,
        <ManageTasksIdFromer
          context={RightContext}
          typeKey="tasks"
          emptyText={getEmptyText(
            { name: "tasks", side: "second" },
            { name: "duties", side: "first" },
          )}
        />,
      ]}
    />
  );
}
