/* eslint-disable @typescript-eslint/no-unused-vars */
import { UUID, DateTime, Duration } from "./helpers";
/* eslint-enable @typescript-eslint/no-unused-vars */

export interface Task {
  name: string;
  duration: Duration;
  description: string;
  depends: Array<string>;
  engagement: number;
}

export interface RunState {
  id: UUID;
  report: DateTime;
  complete: DateTime;
  duties: Array<UUID>;
  tasks: Array<UUID>;
}
