import React, { ForwardRefExoticComponent, RefAttributes } from "react";
import { rem } from "@mantine/core";
import {
  Icon as TablerIcon,
  IconProps as TablerIconProps,
  IconPlayerTrackNextFilled,
} from "@tabler/icons-react";

type IconType = ForwardRefExoticComponent<
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
}

export function Icon({ definition, size }: IconProps) {
  return React.createElement(definition, {
    style: {
      width: rem((size || Size.Medium) as number),
      height: rem((size || Size.Medium) as number),
    },
  });
}

export const Next = IconPlayerTrackNextFilled;
