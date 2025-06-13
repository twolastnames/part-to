import React from "react";

import { Carousel } from "../Carousel/Carousel";
import { MultipleProps } from "../MultipleTypes";

export function Detail({ items, context, pausedByDefault }: MultipleProps) {
  return (
    <span data-testid="Detail">
      <Carousel
        pausedByDefault={pausedByDefault}
        context={context}
        items={items}
      />
    </span>
  );
}
