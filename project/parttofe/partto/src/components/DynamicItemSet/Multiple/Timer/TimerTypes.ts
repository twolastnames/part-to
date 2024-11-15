import { DateTime, Duration } from "../../../../api/helpers";

export interface TimerProps {
  start: DateTime;
  duration: Duration;
  label: string;
  title: string;
  onClick: () => void;
}
