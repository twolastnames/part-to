import React, {
  createContext,
  useState,
  Context,
  MutableRefObject,
  createRef,
  useContext,
  SetStateAction,
} from "react";
import { PropsWithChildren } from "react";
import { Duration, getDuration } from "../shared/duration";
import { debounce, DebouncedFunc } from "lodash";

export type DynamicItemSetPairType = {
  selected: number;
  setSelected: (selected: number) => void;
  getTotal: () => number;
  goBack: () => void;
  goForward: () => void;
  showDuration: Duration;
  togglePause: () => void;
  paused: boolean;
  nextShowDuration: () => void;
};

export const UndefinedDynamicItemSetPair = {
  selected: 0,
  setSelected: (_: number) => undefined,
  goBack: () => undefined,
  goForward: () => undefined,
  getTotal: () => 0,
  showDuration: getDuration(0),
  togglePause: () => undefined,
  paused: true,
  nextShowDuration: () => undefined,
};

export function useSingleOfPair({ context }: ContextDescription) {
  return useContext(context) || UndefinedDynamicItemSetPair;
}

type ContextType = Context<undefined | DynamicItemSetPairType>;

export type ContextDescription = {
  context: ContextType;
  setCount: (value: number) => void;
  setSettingKey: (settingKey: string) => void;
  setDurations: (value: Array<Duration>) => void;
};

const defaultDurations = [1000, 2000, 4000, 8000];

const getDurations = (key: string) =>
  JSON.parse(
    localStorage.getItem(`${key}Durations`) || JSON.stringify(defaultDurations),
  ).map(getDuration);

const setDurations = (key: string, value: Array<Duration>) => {
  localStorage.setItem(
    `${key}Durations`,
    JSON.stringify(value.map((duration) => duration.toMilliseconds())),
  );
};

const leftCount: MutableRefObject<((value: number) => void) | null> =
  createRef();
const leftSettingKey: MutableRefObject<string | null> = createRef();
const getLeftSettingKey = () => leftSettingKey.current || "left";
function setLeftCount(value: number) {
  leftCount.current && leftCount.current(value);
}
const LeftDynamicItemSetPairContext: ContextType = createContext<
  undefined | DynamicItemSetPairType
>(undefined);

export const LeftContext: ContextDescription = {
  context: LeftDynamicItemSetPairContext,
  setCount: setLeftCount,
  setSettingKey: (value: string) => {
    leftSettingKey.current = value;
  },
  setDurations: (value: Array<Duration>) => {
    setDurations(getLeftSettingKey(), value);
  },
};

const rightCount: MutableRefObject<((value: number) => void) | null> =
  createRef();
const rightSettingKey: MutableRefObject<string | null> = createRef();
const getRightSettingKey = () => leftSettingKey.current || "left";

function setRightCount(value: number) {
  rightCount.current && rightCount.current(value);
}
const RightDynamicItemSetPairContext: ContextType = createContext<
  undefined | DynamicItemSetPairType
>(undefined);

export const RightContext: ContextDescription = {
  context: RightDynamicItemSetPairContext,
  setCount: setRightCount,
  setSettingKey: (value: string) => {
    rightSettingKey.current = value;
  },
  setDurations: (value: Array<Duration>) => {
    setDurations(getRightSettingKey(), value);
  },
};

type GoADirection = (
  totalPages: number,
  setSelected: (mutator: (arg: ProviderState) => ProviderState) => void,
) => void;

const goBack: GoADirection = (length, setState) => {
  setState((last: ProviderState) => ({
    ...last,
    selected: last.selected <= 0 ? length - 1 : last.selected - 1,
  }));
};

const goForward: GoADirection = (length, setState) => {
  setState((last: ProviderState) => ({
    ...last,
    selected: last.selected >= length - 1 ? 0 : last.selected + 1,
  }));
};

type ProviderState = {
  selected: number;
  showDuration: number;
  paused: boolean;
  count: number;
};

function useProvider({
  setCount,
  getSettingKey,
  togglePauseClickSlower,
}: {
  getSettingKey: () => string;
  setCount: MutableRefObject<((value: number) => void) | null>;
  togglePauseClickSlower: DebouncedFunc<
    (setState: (arg: SetStateAction<ProviderState>) => void) => void
  >;
}) {
  const durations = getDurations(getSettingKey());
  const [{ count, selected, showDuration, paused }, setState] =
    useState<ProviderState>({
      selected: 0,
      showDuration: Math.floor(durations.length / 2),
      paused: false,
      count: 0,
    });

  setCount.current = (value: number) => {
    if (value === count) {
      return;
    }
    setState((previous) => ({ ...previous, count: value }));
  };

  if (selected !== 0 && (selected < 0 || selected >= count)) {
    setState((current) => ({ ...current, selected: 0 }));
  }

  const duration = durations[showDuration];
  return {
    selected: selected,
    setSelected: (selected: number) => {
      setState((current) => ({ ...current, selected }));
    },
    goBack: () => {
      goBack(count, setState);
    },
    goForward: () => {
      goForward(count, setState);
    },
    showDuration: duration,
    paused: paused,
    getTotal: () => count,
    togglePause: () => {
      togglePauseClickSlower(setState);
    },
    nextShowDuration: () => {
      const next = showDuration + 1;
      setState((previous) => ({
        ...previous,
        showDuration: next >= durations.length ? 0 : next,
      }));
    },
  };
}

const leftTogglePauseClickSlower = debounce(
  (setState: (arg: SetStateAction<ProviderState>) => void) => {
    setState((previous) => ({ ...previous, paused: !previous.paused }));
  },
  100,
);

export function LeftDynamicItemSetPairProvider({
  children,
}: PropsWithChildren) {
  return (
    <LeftDynamicItemSetPairContext.Provider
      value={useProvider({
        setCount: leftCount,
        getSettingKey: getLeftSettingKey,
        togglePauseClickSlower: leftTogglePauseClickSlower,
      })}
    >
      {children}
    </LeftDynamicItemSetPairContext.Provider>
  );
}

const rightTogglePauseClickSlower = debounce(
  (setState: (arg: SetStateAction<ProviderState>) => void) => {
    setState((previous) => ({ ...previous, paused: !previous.paused }));
  },
  100,
);

export function RightDynamicItemSetPairProvider({
  children,
}: PropsWithChildren) {
  return (
    <RightDynamicItemSetPairContext.Provider
      value={useProvider({
        setCount: rightCount,
        getSettingKey: getRightSettingKey,
        togglePauseClickSlower: rightTogglePauseClickSlower,
      })}
    >
      {children}
    </RightDynamicItemSetPairContext.Provider>
  );
}
