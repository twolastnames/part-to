import React from "react";

import classes from "./Timeline.module.scss";
import { TimelineProps, EventProps } from "./TimelineTypes";
import { Accordion } from "../../Accordion/Accordion";
import { DurationFormat, getDuration } from "../../../shared/duration";
import { useTaskGet } from "../../../api/taskget";
import { useRunGet } from "../../../api/runget";
import { getDateTime } from "../../../shared/dateTime";

function Event({ till, task }: EventProps) {
  const response = useTaskGet({ task });
  const description = response?.data?.description || "Now";
  return (
    <>
      <dt>{till.format(DurationFormat.SHORT)}</dt>
      <dd>{description}</dd>
    </>
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
        <div>Duration: {duration?.toString()}</div>
        <div>Completed: {completed.toISOString()}</div>
      </div>
      <Accordion summary="Timeline Estimation">
        <dl>
          {upcoming.map(({ till, task }) => (
            <Event till={till} task={task} />
          ))}
          <dt>{duration?.format(DurationFormat.SHORT)}</dt>
          <dd>Part To Dinner</dd>
        </dl>
      </Accordion>
    </>
  );
}
