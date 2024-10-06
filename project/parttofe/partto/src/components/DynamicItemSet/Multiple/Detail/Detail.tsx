import React from "react";

import { MultipleProps } from "../Multiple";
import { Carousel } from "../Carousel/Carousel";

export function Detail({ items }: MultipleProps) {
  return (
    <span data-testid="Detail">
      <Carousel
        pages={items.map(({ detailView, itemOperations }) => ({
          view: detailView,
          operations: itemOperations,
        }))}
      />
    </span>
  );
}
