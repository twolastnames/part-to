import { useParams } from "react-router-dom";
import { useRunGet } from "../api/runget";
import { Stage } from "../api/helpers";
import { broadcastRunState } from "../shared/runStateMessage";

export function useRunState() {
  const { runState } = useParams();
  const response = useRunGet(
    { runState: runState || "" },
    { shouldSkip: () => !runState },
  );
  if (response.stage === Stage.Ok && response.data) {
    broadcastRunState(response.data);
  }
  return response;
}
