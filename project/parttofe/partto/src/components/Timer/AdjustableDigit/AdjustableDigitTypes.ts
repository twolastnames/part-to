import { PropsWithChildren } from "react";

export interface AdjustableDigitProps extends PropsWithChildren {
  increment?: () => void;
  decrement?: () => void;
}
