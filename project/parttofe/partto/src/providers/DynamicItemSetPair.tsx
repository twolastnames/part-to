import React, {
  createContext,
  useState,
  Context,
  MutableRefObject,
  createRef,
  useContext,
  useCallback,
} from "react";
import { PropsWithChildren } from "react";
import { Duration, getDuration } from "../shared/duration";
import { debounce } from "lodash";

export type DynamicItemSetPairType = {
  selected: number;
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

const leftCount: MutableRefObject<number | null> = createRef();
const leftSettingKey: MutableRefObject<string | null> = createRef();
const getLeftSettingKey = () => leftSettingKey.current || "left";
function setLeftCount(value: number) {
  leftCount.current = value;
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

const rightCount: MutableRefObject<number | null> = createRef();
const rightSettingKey: MutableRefObject<string | null> = createRef();
const getRightSettingKey = () => leftSettingKey.current || "left";

function setRightCount(value: number) {
  rightCount.current = value;
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
};

function useProvider({
  count,
  getSettingKey,
}: {
  getSettingKey: () => string;
  count: MutableRefObject<number | null>;
}) {
  const durations = getDurations(getSettingKey());
  const [state, setState] = useState<ProviderState>({
    selected: 0,
    showDuration: Math.floor(durations.length / 2),
    paused: false,
  });

  const togglePauseClickSlower: () => void = useCallback(
    () =>
      debounce(() => {
        setState((previous) => ({ ...previous, paused: !previous.paused }));
      }, 100)(),
    [],
  );

  if (state.selected < 0) {
    setState((current) => ({ ...current, selected: 0 }));
  } else if (count.current && state.selected >= count.current) {
    setState((current) => ({ ...current, selected: (count.current || 1) - 1 }));
  }
  const duration = durations[state.showDuration];
  return {
    selected: state.selected,
    goBack: () => {
      count.current && goBack(count.current, setState);
    },
    goForward: () => {
      count.current && goForward(count.current, setState);
    },
    showDuration: duration,
    paused: state.paused,
    getTotal: () => count.current || 0,
    togglePause: () => {
      togglePauseClickSlower();
    },
    nextShowDuration: () => {
      const next = state.showDuration + 1;
      setState((previous) => ({
        ...previous,
        showDuration: next >= durations.length ? 0 : next,
      }));
    },
  };
}

export function LeftDynamicItemSetPairProvider({
  children,
}: PropsWithChildren) {
  return (
    <LeftDynamicItemSetPairContext.Provider
      value={useProvider({
        count: leftCount,
        getSettingKey: getLeftSettingKey,
      })}
    >
      {children}
    </LeftDynamicItemSetPairContext.Provider>
  );
}

export function RightDynamicItemSetPairProvider({
  children,
}: PropsWithChildren) {
  return (
    <RightDynamicItemSetPairContext.Provider
      value={useProvider({
        count: rightCount,
        getSettingKey: getRightSettingKey,
      })}
    >
      {children}
    </RightDynamicItemSetPairContext.Provider>
  );
}
