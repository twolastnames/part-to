import React from "react";

import classes from "./Timeline.module.scss";
import { TimelineProps, EventProps } from "./TimelineTypes";
import { Accordion } from "../../Accordion/Accordion";
import { DurationFormat, getDuration } from "../../../shared/duration";
import { useTaskGet } from "../../../api/taskget";
import { useRunGet } from "../../../api/runget";
import { Format, getDateTime } from "../../../shared/dateTime";
import { Title } from "../../Title/Title";
import { TaskTitle } from "./TaskTitle/TaskTitle";
import { PartTo } from "../../Icon/Icon";

function Event({ task, runState }: EventProps) {
  const taskResponse = useTaskGet({ task });
  const runStateResponse = useRunGet({ runState });
  const description = taskResponse?.data?.description || "Now";
  if (!taskResponse.data || !runStateResponse.data) {
    return <></>;
  }
  return (
    <div className={classes.entry}>
      <dt>
        <TaskTitle task={task} runState={runState} />
      </dt>
      <dd>{description}</dd>
    </div>
  );
}

export function Timeline({ runState }: TimelineProps) {
  const response = useRunGet({ runState });
  const upcoming = response?.data?.upcoming || [];
  const duration = response?.data?.duration;
  const completed = getDateTime().add(duration || getDuration(0));

  return (
    <>
      <div className={classes.time}>
        <div>Estimated Meal Time: {completed.format(Format.TIME)}</div>
      </div>
      <Accordion summary="Timeline Estimation">
        <dl className={classes.timeline}>
          {upcoming.map(({ task }) => (
            <Event runState={runState} task={task} />
          ))}
          <Title icon={PartTo}>{duration?.format(DurationFormat.SHORT)}</Title>
          <dd>Part To</dd>
        </dl>
      </Accordion>
    </>
  );
}
