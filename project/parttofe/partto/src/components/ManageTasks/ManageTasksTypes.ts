import { RunStateId, TaskDefinitionId } from "../../api/sharedschemas";
import { ContextDescription } from "../../providers/DynamicItemSetPair";

export interface ManageTasksProps {
  tasks: Array<TaskDefinitionId>;
  runState: RunStateId;
  emptyText: string;
  context: ContextDescription;
}
