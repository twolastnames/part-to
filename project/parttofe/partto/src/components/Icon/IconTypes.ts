import {
  Icon as TablerIcon,
  IconProps as TablerIconProps,
} from "@tabler/icons-react";
import { ForwardRefExoticComponent, RefAttributes } from "react";

export type IconType = ForwardRefExoticComponent<
  TablerIconProps & RefAttributes<TablerIcon>
>;

export enum Size {
  Small = 20,
  Medium = 30,
  Large = 50,
  ExtraLarge = 80,
}

export interface IconProps {
  definition: IconType;
  size?: Size;
  onClick?: () => void;
}
