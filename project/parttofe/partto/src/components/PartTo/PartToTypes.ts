import { ReactNode } from "react";
import { Duration } from "../../shared/duration";

export interface PartToProps {
  name: string;
  workDuration?: Duration;
  clockDuration?: Duration;
  tasks: Array<ReactNode>;
}
