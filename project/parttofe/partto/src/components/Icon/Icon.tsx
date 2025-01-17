import React from "react";
import { rem } from "@mantine/core";
import {
  IconPlayerTrackNext,
  IconPlayerPlay,
  IconList,
  IconFile,
  IconCaretDown,
  IconCaretUp,
  IconChefHat,
  IconBook,
  IconCooker,
  IconToolsKitchen,
  IconSettings,
  IconInfoSquareRounded,
  IconMoodEmpty,
  IconPlus,
  IconCancel,
  IconCheck,
  IconEye,
  IconChecklist,
  IconPlaneArrival,
  IconBowlSpoon,
} from "@tabler/icons-react";

import classes from "./Icon.module.scss";
import { IconProps, Size } from "./IconTypes";

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
      color: "var(--detail-color)",
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
export const Book = IconBook;
export const Settings = IconSettings;
export const Info = IconInfoSquareRounded;
export const Empty = IconMoodEmpty;
export const Plus = IconPlus;
export const Cancel = IconCancel;
export const Check = IconCheck;
export const Duty = IconEye;
export const Task = IconChecklist;
export const Imminent = IconPlaneArrival;
export const Recipe = IconBowlSpoon;
