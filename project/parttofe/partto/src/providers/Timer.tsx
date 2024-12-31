import React, {
  createContext,
  ReactNode,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";
import { PropsWithChildren } from "react";
import { DateTime, getDateTime } from "../shared/dateTime";
import { Duration, getDuration } from "../shared/duration";
import { RunState, TaskDefinitionId } from "../api/sharedschemas";
import { Timer } from "../components/Timer/Timer";
import {
  addAlarmNote,
  removeNote,
} from "../components/Layout/NavigationBar/Noted/Noted";
import {
  addRunStateListener,
  removeRunStateListener,
} from "../shared/runStateMessage";

type TimerDescription = {
  component: ReactNode;
  duration: Duration;
  started: DateTime;
  message: string;
  enforced: boolean;
  task: TaskDefinitionId;
  setOnLocate: (callback: () => void) => void;
};

export type TimerType = {
  timers: { [id: string]: TimerDescription };
};

export const TimerContext = createContext<undefined | TimerType>(undefined);

type TaskKeyed = { task: TaskDefinitionId };

type TimerFactory<T> = (args: T) => {
  component: ReactNode;
  duration: Duration;
  task: TaskDefinitionId;
};

function getMappedTimers<T extends TaskKeyed>(
  getTimer: TimerFactory<T>,
  timers: Array<T> | undefined,
): { [id: string]: TimerDescription } {
  return (
    timers?.reduce(
      (current, timer) => ({
        ...current,
        [timer.task]: getTimer(timer),
      }),
      {},
    ) || ({} as { [id: TaskDefinitionId]: T })
  );
}

export function TimerProvider({ children }: PropsWithChildren) {
  const [runState, setRunState] = useState<RunState | undefined>();
  const offsets = useRef<{
    [id: string]: Duration;
  }>({});
  const onLocates = useRef<{ [task: string]: () => void }>({});
  const audio = useRef(new Audio(require("./messageAlert.mp3")));
  const timestamp = runState?.timestamp;
  const timers = useMemo(
    () => ({
      ...getMappedTimers(
        ({ task, started, duration }) => ({
          task,
          started,
          setOnLocate: (callback: () => void) => {
            onLocates.current[task] = callback;
          },
          duration,
          enforced: true,
          message: "Duty Complete?",
          component: (
            <Timer
              start={started}
              duration={duration}
              adjustment={{
                offset: offsets.current[task] || getDuration(0),
                setOffset: (value: Duration) => (offsets.current[task] = value),
              }}
            />
          ),
        }),
        runState?.timers.enforced || [],
      ),
      ...getMappedTimers(
        ({ task, started, duration }) => ({
          task,
          started,
          setOnLocate: (callback: () => void) => {
            onLocates.current[task] = callback;
          },
          duration,
          enforced: false,
          message: "Past Expected Time",
          component: <Timer start={started} duration={duration} />,
        }),
        runState?.timers.laxed || [],
      ),
      ...getMappedTimers(
        ({ task, till }) => ({
          task,
          started: timestamp,
          setOnLocate: (callback: () => void) => {
            onLocates.current[task] = callback;
          },
          duration: till,
          enforced: true,
          message: "Need to Start Duty",
          component: <Timer start={timestamp} duration={till} />,
        }),
        runState?.timers.imminent || [],
      ),
    }),
    [runState, offsets, timestamp],
  );

  useEffect(() => {
    addRunStateListener(setRunState);
    return () => {
      removeRunStateListener(setRunState);
    };
  }, [setRunState]);

  useEffect(() => {
    const id = setInterval(() => {
      const now = getDateTime();
      for (const [key, timer] of Object.entries(timers)) {
        const expireAt = timer.started
          .add(offsets.current[key] || getDuration(0))
          .add(timer.duration);
        if (!timer.enforced || now.sinceEpoch() < expireAt.sinceEpoch()) {
          continue;
        }
        addAlarmNote({
          key,
          heading: "Alarm Expired",
          detail: timer.message,
          onClick: () => {
            onLocates.current[key]?.();
          },
        });
        if (!audio.current.paused) {
          return;
        }
        try {
          audio.current.play();
        } catch (NotAllowedError) {
          console.error(
            "could not start an alarm... likely because the page has not been interacted with",
          );
        }
        audio.current.loop = true;
        return;
      }
      for (const key of Object.keys(timers)) {
        removeNote(key);
      }
      audio.current.pause();
    }, 1000);
    return () => {
      clearInterval(id);
    };
  }, [offsets, runState, timers]);

  return (
    <TimerContext.Provider
      value={{
        timers,
      }}
    >
      {children}
    </TimerContext.Provider>
  );
}

export function useTimerProvider({
  task,
  onLocate,
}: {
  task: TaskDefinitionId;
  onLocate?: () => void;
}) {
  const timers = useContext(TimerContext)?.timers;
  onLocate && timers?.[task]?.setOnLocate(onLocate);
  return timers?.[task]?.component || <></>;
}
