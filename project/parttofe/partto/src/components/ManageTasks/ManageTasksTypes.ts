import { RunState, TaskDefinitionId } from "../../api/sharedschemas";
import { ContextDescription } from "../../providers/DynamicItemSetPair";
import { NavigateFunction } from "react-router-dom";
import { Item } from "../DynamicItemSet/DynamicItemSetTypes";
import { ClassNames } from "../TaskDefinition/TaskDefinitionTypes";

export type RunStateItemGetter = (
  navigate: NavigateFunction,
  runState: RunState,
  context: ContextDescription,
  mapIndex: (value: number) => number,
) => Array<Item>;

export interface ManageTasksProps {
  tasks: Array<TaskDefinitionId>;
  emptyText: string;
  context: ContextDescription;
  getPrependedItems?: RunStateItemGetter;
  definitionClassNames: ClassNames;
}
