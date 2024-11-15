import React from "react";

import { Carousel } from "../Carousel/Carousel";
import { MultipleProps } from "../MultipleTypes";

export function Detail({ items }: MultipleProps) {
  return (
    <span data-testid="Detail">
      <Carousel items={items} />
    </span>
  );
}
