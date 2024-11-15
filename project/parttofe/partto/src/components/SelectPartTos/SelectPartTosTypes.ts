import { MutableRefObject } from "react";
import { RunStateId } from "../../api/sharedschemas";

export interface SelectPartTosProps {
  runState?: MutableRefObject<RunStateId>;
}
