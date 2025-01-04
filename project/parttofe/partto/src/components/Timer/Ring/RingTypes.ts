import { ReactNode } from "react";

export type ClassNames = {
  progress: string;
};

export interface RingProps {
  magnitude: number;
  label: ReactNode;
  classNames: ClassNames;
}
