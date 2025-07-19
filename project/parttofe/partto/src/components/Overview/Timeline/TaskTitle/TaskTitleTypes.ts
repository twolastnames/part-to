import { RunStateId, TaskDefinitionId } from "../../../../api/sharedschemas";

export interface TaskTitleProps {
  task: TaskDefinitionId;
  runState: RunStateId;
}
