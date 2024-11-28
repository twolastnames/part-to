import { RunStateId, TaskDefinitionId } from "../../../api/sharedschemas";

export interface DetailProps {
  task: TaskDefinitionId;
  runState: RunStateId;
}
