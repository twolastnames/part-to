import { ReactNode } from "react";
import { RunStateId, TaskDefinitionId } from "../../../api/sharedschemas";
import { ClassNames } from "../Icon/IconTypes";

export type IconClassSets = {
  imminent: ClassNames;
  duty: ClassNames;
  task: ClassNames;
};

export interface ListItemProps {
  task: TaskDefinitionId;
  runState: RunStateId;
  precursor?: ReactNode;
  iconClassSets: IconClassSets;
}
