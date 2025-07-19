import { ContextDescription } from "../../../providers/DynamicItemSetPair";
import { Item } from "../DynamicItemSetTypes";

export interface MultipleProps {
  items: Array<Item>;
  context: ContextDescription;
  pausedByDefault?: boolean;
}
