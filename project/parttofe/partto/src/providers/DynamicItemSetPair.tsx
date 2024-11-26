import React, {
  createContext,
  useState,
  Context,
  MutableRefObject,
  createRef,
} from "react";
import { PropsWithChildren } from "react";

export type DynamicItemSetPairType = {
  selected: number;
  goBack: () => void;
  goForward: () => void;
};

export const UndefinedDynamicItemSetPair = {
  selected: -1,
  goBack: () => undefined,
  goForward: () => undefined,
};

type ContextType = Context<undefined | DynamicItemSetPairType>;

export type ContextDescription = {
  context: ContextType;
  setCount: (value: number) => void;
};

const leftCount: MutableRefObject<number | null> = createRef();
function setLeftCount(value: number) {
  leftCount.current = value;
}
const LeftDynamicItemSetPairContext: ContextType = createContext<
  undefined | DynamicItemSetPairType
>(undefined);

export const LeftContext: ContextDescription = {
  context: LeftDynamicItemSetPairContext,
  setCount: setLeftCount,
};

const rightCount: MutableRefObject<number | null> = createRef();
function setRightCount(value: number) {
  rightCount.current = value;
}
const RightDynamicItemSetPairContext: ContextType = createContext<
  undefined | DynamicItemSetPairType
>(undefined);

export const RightContext: ContextDescription = {
  context: RightDynamicItemSetPairContext,
  setCount: setRightCount,
};

type GoADirection = (
  totalPages: number,
  setSelected: (
    mutator: (arg: DynamicItemSetPairType) => DynamicItemSetPairType,
  ) => void,
) => void;

const goBack: GoADirection = (length, setState) => {
  setState((last: DynamicItemSetPairType) => ({
    ...last,
    selected: last.selected <= 0 ? length - 1 : last.selected - 1,
  }));
};

const goForward: GoADirection = (length, setState) => {
  setState((last: DynamicItemSetPairType) => ({
    ...last,
    selected: last.selected >= length - 1 ? 0 : last.selected + 1,
  }));
};

function useProvider({ count }: { count: MutableRefObject<number | null> }) {
  const [state, setState] = useState<DynamicItemSetPairType>({
    selected: 0,
    goBack: () => {
      count.current && goBack(count.current, setState);
    },
    goForward: () => {
      count.current && goForward(count.current, setState);
    },
  });
  return state;
}

export function LeftDynamicItemSetPairProvider({
  children,
}: PropsWithChildren) {
  return (
    <LeftDynamicItemSetPairContext.Provider
      value={useProvider({ count: leftCount })}
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
      value={useProvider({ count: rightCount })}
    >
      {children}
    </RightDynamicItemSetPairContext.Provider>
  );
}
