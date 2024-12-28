import { RunState } from "../api/sharedschemas";

let LocalMessageChannel;
try {
  // eslint-disable-next-line
  LocalMessageChannel = MessageChannel;
} catch {
  // likely in node here (unit tests)
}

try {
  // eslint-disable-next-line
  LocalMessageChannel = require("worker_threads").MessageChannel;
} catch {
  //   likely in a browser here
}

const runStateChannel = new LocalMessageChannel();

type Listener = {
  unparsed: (message: MessageEvent<string>) => void;
  parsed: (runState: RunState) => void;
};

let listeners: Array<Listener> = [];

let lastRunState: RunState;

export function addRunStateListener(listener: (runState: RunState) => void) {
  const unparsedListener = (unparsed: MessageEvent<string>) => {
    listener(JSON.parse(unparsed.data));
  };
  if (listeners.some(({ unparsed }) => unparsedListener === unparsed)) {
    return;
  }
  lastRunState && listener(lastRunState);
  listeners.push({ unparsed: unparsedListener, parsed: listener });
  runStateChannel.port1.addEventListener("message", unparsedListener);
}

export function removeRunStateListener(listener: (runState: RunState) => void) {
  const removable = listeners.find(({ parsed }) => parsed === listener);
  if (!removable) {
    return;
  }
  runStateChannel.port1.removeEventListener("message", removable.unparsed);
  listeners = listeners.filter(({ parsed }) => parsed === listener);
}

export function broadcastRunState(runState: RunState) {
  lastRunState = runState;
  runStateChannel.port2.postMessage(JSON.stringify(runState));
}
