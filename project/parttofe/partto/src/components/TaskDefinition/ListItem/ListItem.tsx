import React from "react";

import { ListItemProps } from "./ListItemTypes";
import { Spinner } from "../../Spinner/Spinner";
import { useRunGet } from "../../../api/runget";
import { Icon } from "../Icon/Icon";
import { useTaskGet } from "../../../api/taskget";
import { ListItem as GenericListItem } from "../../ListItem/ListItem";

export function ListItem({ task, runState, iconClassSets }: ListItemProps) {
  const taskResponse = useTaskGet({ task });
  const response = useRunGet({ runState });

  const iconClasses = response.data?.timers.imminent
    .map((timer) => timer.task)
    .includes(task)
    ? iconClassSets.imminent
    : response?.data?.duties.includes(task)
      ? iconClassSets.duty
      : iconClassSets.task;

  return (
    <Spinner responses={[response]}>
      <GenericListItem
        precursor={<Icon classNames={iconClasses} />}
        description={taskResponse.data?.description}
      />
    </Spinner>
  );
}
