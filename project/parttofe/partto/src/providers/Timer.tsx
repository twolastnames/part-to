import React, {
  createContext,
  createRef,
  MutableRefObject,
  useContext,
  useState,
} from "react";
import { PropsWithChildren } from "react";
import { DateTime } from "../shared/dateTime";
import { Duration } from "../shared/duration";

export type TimerType = {
  timers: TimerSet;
  add: (id: string, start: DateTime, duration: Duration) => void;
  clear: () => void;
};

type TimerDescription = {
  start: DateTime;
  duration: Duration;
};

export interface TimerSet {
  [key: string]: TimerDescription;
}

export const timerClearer: MutableRefObject<undefined | null | (() => void)> =
  createRef<undefined | (() => void)>();

export const clearTimers = () => {
  timerClearer.current && timerClearer.current();
};

export const TimerContext = createContext<undefined | TimerType>(undefined);

export function TimerProvider({ children }: PropsWithChildren) {
  const [timers, setTimers] = useState<TimerSet>({});
  timerClearer.current = () => {
    setTimers({});
  };
  return (
    <TimerContext.Provider
      value={{
        timers,
        add: (id, start, duration) => {
          if (
            Object.keys(timers).includes(id) &&
            timers[id].duration === duration &&
            timers[id].start === start
          ) {
            return;
          }
          setTimers((previous) => ({ ...previous, [id]: { start, duration } }));
        },
        clear: () => {
          setTimers({});
        },
      }}
    >
      {children}
    </TimerContext.Provider>
  );
}

export function useTimerProvider() {
  return (
    useContext(TimerContext) || {
      timers: {},
      add: () => undefined,
    }
  );
}
