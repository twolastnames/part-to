import React from "react";

import { Carousel } from "../Carousel/Carousel";
import { MultipleProps } from "../MultipleTypes";

export function Detail({ items, context }: MultipleProps) {
  return (
    <span data-testid="Detail">
      <Carousel context={context} items={items} />
    </span>
  );
}
