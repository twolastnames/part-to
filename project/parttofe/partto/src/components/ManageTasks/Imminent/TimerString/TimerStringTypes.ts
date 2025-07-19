import { DateTime } from "../../../../shared/dateTime";
import { Duration } from "../../../../shared/duration";

export interface TimerStringProps {
  duration: Duration;
  started: DateTime;
}
