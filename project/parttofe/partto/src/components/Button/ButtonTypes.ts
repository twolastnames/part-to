import { IconType } from "../Icon/IconTypes";

export interface ButtonProps {
  text: string;
  icon: IconType;
  onClick: () => void;
}
