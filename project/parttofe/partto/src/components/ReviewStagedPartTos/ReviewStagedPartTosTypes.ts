import { MutableRefObject } from "react";
import { RunStateId, TaskDefinitionId } from "../../api/sharedschemas";

export interface ReviewStagedPartTosProps {
  taskDefinitions: Array<TaskDefinitionId>;
  runState: MutableRefObject<RunStateId>;
}
