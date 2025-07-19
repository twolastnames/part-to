import { ContextDescription } from "../../providers/DynamicItemSetPair";
import { IconType } from "../Icon/IconTypes";

export interface Operation {
  text: string;
  icon: IconType;
  onClick: () => void;
}

export interface Item {
  key: string;
  listView: React.ReactElement;
  detailView: React.ReactElement;
  itemOperations: Array<Operation>;
}

export interface DynamicItemSetProps {
  items: Array<Item>;
  setOperations: Array<Operation>;
  emptyPage: React.ReactElement;
  context: ContextDescription;
  pausedByDefault?: boolean;
}
