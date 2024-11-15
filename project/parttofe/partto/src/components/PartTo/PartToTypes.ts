import { ReactNode } from "react";
import { Duration } from "../../api/helpers";

export interface PartToProps {
  name: string;
  workDuration?: Duration;
  clockDuration?: Duration;
  tasks: Array<ReactNode>;
}
