export interface IterationProgressProps {
  setPaused: (arg: boolean) => void;
  paused: boolean;
  showDuration: number;
  total: number;
  setShowDuration: (arg: number) => void;
  on: number;
}
