import React, { ForwardRefExoticComponent, RefAttributes } from "react";
import { rem } from "@mantine/core";
import {
  Icon as TablerIcon,
  IconProps as TablerIconProps,
  IconPlayerTrackNext,
  IconPlayerPlay,
  IconList,
  IconFile,
  IconCaretDown,
  IconCaretUp,
  IconChefHat,
  IconCooker,
  IconToolsKitchen,
} from "@tabler/icons-react";

import classes from "./Icon.module.scss";

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

export function Icon({ onClick, definition, size }: IconProps) {
  return React.createElement(definition, {
    ...(onClick
      ? {
          onClick,
          className: classes.clickable,
        }
      : {}),
    style: {
      width: rem((size || Size.Medium) as number),
      height: rem((size || Size.Medium) as number),
    },
  });
}

export const Next = IconPlayerTrackNext;
export const Start = IconPlayerPlay;
export const List = IconList;
export const File = IconFile;
export const Up = IconCaretUp;
export const Down = IconCaretDown;
export const ChefHat = IconChefHat;
export const Oven = IconCooker;
export const KitchenTools = IconToolsKitchen;
