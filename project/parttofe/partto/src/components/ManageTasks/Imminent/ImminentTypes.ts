import { TaskDefinitionId } from "../../../api/sharedschemas";
import { ContextDescription } from "../../../providers/DynamicItemSetPair";
import { DateTime } from "../../../shared/dateTime";
import { Duration } from "../../../shared/duration";

type Locatable = {
  onLocate: (setter: (value: number) => void) => () => void;
  context: ContextDescription;
};

export interface ImminentProps {
  timestamp: DateTime;
  till: Duration;
  duty: TaskDefinitionId;
}
