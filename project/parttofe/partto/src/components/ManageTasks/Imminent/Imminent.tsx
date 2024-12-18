import React from "react";

import { NavigateFunction } from "react-router-dom";
import { RunState } from "../../../api/sharedschemas";
import { Item } from "../../DynamicItemSet/DynamicItemSetTypes";
import { List } from "./List/List";
import { Detail } from "./Detail/Detail";
import { Cancel, Oven } from "../../Icon/Icon";
import { doRunvoidPost } from "../../../api/runvoidpost";
import { getRoute } from "../../../routes";
import { doRunstartPost } from "../../../api/runstartpost";

export function getImminentItems(
  navigate: NavigateFunction,
  { timestamp, imminent, runState }: RunState,
): Array<Item> {
  return imminent.map(({ till, duty }) => ({
    key: duty,
    listView: <List timestamp={timestamp} till={till} duty={duty} />,
    detailView: <Detail timestamp={timestamp} till={till} duty={duty} />,
    itemOperations: [
      {
        text: "Skip and Void",
        icon: Cancel,
        onClick: () => {
          doRunvoidPost({
            body: {
              runState,
              definitions: [duty],
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
              definitions: [duty],
            },
            on200: ({ runState }) => {
              navigate(getRoute("CookMeal", { runState }));
            },
          });
        },
      },
    ],
  }));
}
