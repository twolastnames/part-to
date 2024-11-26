import { DateTime } from "../../../../shared/dateTime";
import { Duration } from "../../../../shared/duration";

export interface TimerProps {
  start: DateTime;
  duration?: Duration;
  label: string;
  title: string;
  onClick: () => void;
}
