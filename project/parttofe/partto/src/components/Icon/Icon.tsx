import React, { ForwardRefExoticComponent, RefAttributes } from "react";
import { rem } from '@mantine/core';
import { Icon as TablerIcon, IconPlayerTrackNextFilled } from '@tabler/icons-react';

export type IconType = ForwardRefExoticComponent<IconProps & RefAttributes<TablerIcon>>;

export enum Size {
  Small = '20',
  Medium = '30',
  Large = '50',
  ExtraLarge = '80',
}

export interface IconProps { definition: IconType, size?: Size}

export function Icon({definition, size}: IconProps) {
  return React.createElement(definition, {style: {
    width: rem((size || Size.Medium) as unknown as number),
    height: rem((size || Size.Medium) as unknown as number),
  }})
}

export const Next = IconPlayerTrackNextFilled;



