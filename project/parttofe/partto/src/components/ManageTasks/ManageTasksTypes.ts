import { RunState, TaskDefinitionId } from "../../api/sharedschemas";
import { ContextDescription } from "../../providers/DynamicItemSetPair";
import { NavigateFunction } from "react-router-dom";
import { Item } from "../DynamicItemSet/DynamicItemSetTypes";

export type RunStateItemGetter = (
  navigate: NavigateFunction,
  runState: RunState,
) => Array<Item>;

export interface ManageTasksProps {
  tasks: Array<TaskDefinitionId>;
  emptyText: string;
  context: ContextDescription;
  getPrependedItems?: RunStateItemGetter;
}
