import { RunStateId, TaskDefinitionId } from "../../api/sharedschemas";
import { ContextDescription } from "../../providers/DynamicItemSetPair";

type Locatable = {
  onLocate: (setter: (value: number) => void) => () => void;
  context: ContextDescription;
};

export interface DetailProps {
  task: TaskDefinitionId;
  runState: RunStateId;
  locatable: Locatable;
}
