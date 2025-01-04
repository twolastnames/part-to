import { DateTime } from "../../shared/dateTime";
import { Duration } from "../../shared/duration";
import { ClassNames } from "./Ring/RingTypes";

export type Offset = {
  offset: Duration;
  setOffset: (value: Duration) => void;
};

export interface TimerProps {
  start?: DateTime;
  duration: Duration;
  adjustment?: Offset;
  ringClasses: ClassNames;
}
