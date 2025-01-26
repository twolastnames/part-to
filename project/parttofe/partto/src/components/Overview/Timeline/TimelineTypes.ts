import { RunStateId, TaskDefinitionId } from "../../../api/sharedschemas";
import { Duration } from "../../../shared/duration";

export type EventProps = { till: Duration; task: TaskDefinitionId };

export interface TimelineProps {
  runState: RunStateId;
}
