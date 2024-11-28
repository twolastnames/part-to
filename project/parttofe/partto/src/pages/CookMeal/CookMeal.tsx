import React from "react";

import { Layout } from "../../components/Layout/Layout";
import { ManageTasksIdFromer } from "../../components/ManageTasks/ManageTasks";
import { useParams } from "react-router-dom";
import { LeftContext, RightContext } from "../../providers/DynamicItemSetPair";

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
  const { runState } = useParams() as { runState: string };
  return (
    <Layout
      pair={[
        <ManageTasksIdFromer
          runState={runState}
          typeKey="duties"
          context={LeftContext}
          emptyText={getEmptyText(
            { name: "duties", side: "first" },
            { name: "tasks", side: "second" },
          )}
        />,
        <ManageTasksIdFromer
          runState={runState}
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
