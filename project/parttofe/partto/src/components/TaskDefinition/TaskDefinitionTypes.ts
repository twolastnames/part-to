import { RunStateId, TaskDefinitionId } from "../../api/sharedschemas";
import { ContextDescription } from "../../providers/DynamicItemSetPair";

type Locatable = {
  onLocate: (setter: (value: number) => void) => () => void;
  context: ContextDescription;
};

export type ClassNames = {
  layout: string;
  timer: string;
  upcomingTitle: string;
  upcomingDescription: string;
};

export interface TaskDefinitionProps {
  task: TaskDefinitionId;
  runState: RunStateId;
  locatable: Locatable;
  classNames: ClassNames;
}
