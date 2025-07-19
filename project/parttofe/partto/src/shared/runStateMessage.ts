import { RunState } from "../api/sharedschemas";

let listeners: Array<(runState: RunState) => void> = [];

let lastRunState: RunState;

export function addRunStateListener(newListener: (runState: RunState) => void) {
  if (listeners.some((listener) => listener === newListener)) {
    return;
  }
  lastRunState && newListener(lastRunState);
  listeners.push(newListener);
}

export function removeRunStateListener(
  oldListener: (runState: RunState) => void,
) {
  const removable = listeners.find((listener) => oldListener === listener);
  if (!removable) {
    return;
  }
  listeners = listeners.filter((removable) => removable !== oldListener);
}

export function broadcastRunState(runState: RunState) {
  lastRunState = runState;
  for (const listener of listeners) {
    listener(lastRunState);
  }
}
