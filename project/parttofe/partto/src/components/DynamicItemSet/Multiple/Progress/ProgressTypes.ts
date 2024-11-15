export interface ProgressProps {
  on: number;
  total: number;
  label: string;
  title: string;
  onClick: () => void;
}
