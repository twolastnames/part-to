import React from "react";

import { NavigateFunction } from "react-router-dom";
import { RunState } from "../../../api/sharedschemas";
import { Item } from "../../DynamicItemSet/DynamicItemSetTypes";
import { List } from "./List/List";
import { Cancel, Oven } from "../../Icon/Icon";
import { doRunvoidPost } from "../../../api/runvoidpost";
import { getRoute } from "../../../routes";
import { doRunstartPost } from "../../../api/runstartpost";
import { ContextDescription } from "../../../providers/DynamicItemSetPair";
import {
  ImminentClassNames,
  TaskDefinition,
} from "../../TaskDefinition/TaskDefinition";

export function getImminentItems(
  navigate: NavigateFunction,
  { timestamp, timers: { imminent }, runState }: RunState,
  context: ContextDescription,
  mapIndex: (value: number) => number,
): Array<Item> {
  return (
    imminent?.map(({ till, task }, index) => ({
      key: task,
      listView: <List timestamp={timestamp} till={till} duty={task} />,
      detailView: (
        <TaskDefinition
          task={task}
          runState={runState}
          locatable={{
            onLocate: (setter) => () => {
              setter(mapIndex(index));
            },
            context,
          }}
          classNames={ImminentClassNames}
        />
      ),
      itemOperations: [
        {
          text: "Skip and Void",
          icon: Cancel,
          onClick: () => {
            doRunvoidPost({
              body: {
                runState,
                definitions: [task],
              },
              on200: ({ runState }) => {
                navigate(getRoute("CookMeal", { runState }));
              },
            });
          },
        },
        {
          text: "Start Duty",
          icon: Oven,
          onClick: () => {
            doRunstartPost({
              body: {
                runState,
                definitions: [task],
              },
              on200: ({ runState }) => {
                navigate(getRoute("CookMeal", { runState }));
              },
            });
          },
        },
      ],
    })) || []
  );
}
