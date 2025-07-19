import React from "react";

import { TaskTitleProps } from "./TaskTitleTypes";
import { useRunGet } from "../../../../api/runget";
import { DurationFormat, getDuration } from "../../../../shared/duration";
import { Alarmed, Timed } from "../../../Icon/Icon";
import { Title } from "../../../Title/Title";

export function TaskTitle({ runState, task }: TaskTitleProps) {
  const response = useRunGet({ runState });
  const icon = response?.data?.tasks.includes(task) ? Timed : Alarmed;
  const { till, duration } = response?.data?.upcoming.find(
    (event) => event.task === task,
  ) || { till: getDuration(0) };
  return (
    <Title icon={icon}>
      {till.format(DurationFormat.SHORT)}
      {" - "}
      {duration && till.add(duration)?.format(DurationFormat.SHORT)}
    </Title>
  );
}
