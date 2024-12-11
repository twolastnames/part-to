import { MultipleProps } from "../MultipleTypes";

export interface ListProps extends MultipleProps {
  onSelectionChanged: () => void;
}
