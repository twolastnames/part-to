import React from "react";

import classes from "./ListItem.module.scss";
import { ListItemProps } from "./ListItemTypes";
import { Spinner } from "../../Spinner/Spinner";
import { useRunGet } from "../../../api/runget";
import { Icon } from "../Icon/Icon";
import { useTaskGet } from "../../../api/taskget";

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
      <div className={classes.listItem} data-testid="ListItem">
        <Icon classNames={iconClasses} />
        <div className={classes.description}>
          {taskResponse.data?.description}
        </div>
      </div>
    </Spinner>
  );
}
