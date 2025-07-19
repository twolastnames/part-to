import { Duration } from "../../shared/duration";
import { PropsWithChildren, ReactNode } from "react";

export interface PartToProps extends PropsWithChildren {
  name: ReactNode;
  workDuration?: Duration;
  clockDuration?: Duration;
}
