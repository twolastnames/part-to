import React from "react";

import classes from "./Icon.module.scss";
import { ClassNames, IconProps } from "./IconTypes";
import {
  Duty as DutyIcon,
  Imminent as ImminentIcon,
  Icon as PhysicalIcon,
  Task as TaskIcon,
} from "../../Icon/Icon";

export const Duty: ClassNames = {
  imminent: classes.hidden,
  duty: "",
  task: classes.hidden,
};

export const Task: ClassNames = {
  imminent: classes.hidden,
  duty: classes.hidden,
  task: "",
};

export const Imminent: ClassNames = {
  imminent: "",
  duty: classes.hidden,
  task: classes.hidden,
};

export function Icon({ classNames: { task, duty, imminent } }: IconProps) {
  return (
    <>
      <span className={imminent}>
        <PhysicalIcon definition={ImminentIcon} />
      </span>
      <span className={duty}>
        <PhysicalIcon definition={DutyIcon} />
      </span>
      <span className={task}>
        <PhysicalIcon definition={TaskIcon} />
      </span>
    </>
  );
}
