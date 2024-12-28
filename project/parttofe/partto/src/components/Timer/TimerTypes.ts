import { DateTime } from "../../shared/dateTime";
import { Duration } from "../../shared/duration";

export type Offset = {
  offset: Duration;
  setOffset: (value: Duration) => void;
};

export interface TimerProps {
  start?: DateTime;
  duration: Duration;
  adjustment?: Offset;
}
