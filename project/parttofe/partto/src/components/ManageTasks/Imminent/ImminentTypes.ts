import { TaskDefinitionId } from "../../../api/sharedschemas";
import { ContextDescription } from "../../../providers/DynamicItemSetPair";
import { DateTime } from "../../../shared/dateTime";
import { Duration } from "../../../shared/duration";

export interface ImminentProps {
  timestamp: DateTime;
  till: Duration;
  duty: TaskDefinitionId;
}
