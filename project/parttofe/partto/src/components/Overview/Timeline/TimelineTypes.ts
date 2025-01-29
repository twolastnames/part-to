import { RunStateId, TaskDefinitionId } from "../../../api/sharedschemas";

export type EventProps = { runState: RunStateId; task: TaskDefinitionId };

export interface TimelineProps {
  runState: RunStateId;
}
