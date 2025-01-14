import { Duration } from "../../shared/duration";
import { PropsWithChildren } from "react";

export interface PartToProps extends PropsWithChildren {
  name: string;
  workDuration?: Duration;
  clockDuration?: Duration;
}
