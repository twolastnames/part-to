import React, { useLayoutEffect, useRef, useState } from "react";

import classes from "./Ring.module.scss";
import { RingProps } from "./RingTypes";
import { RingProgress } from "@mantine/core";
import { useWindowResize } from "../../../hooks/windowResize";

export function Ring({ magnitude, label }: RingProps) {
  const { height, width } = useWindowResize();
  const [size /* TODO: reimplment here */] = useState<number>(1);
  const ringRef = useRef<HTMLDivElement | null>(null);

  const color1 =
    magnitude >= 1 ? "var(--highlight-color)" : "var(--secondary-color)";
  const value1 = magnitude >= 2 ? 1 : magnitude % 1;
  const color2 =
    magnitude >= 1 ? "var(--secondary-color)" : "var(--highlight-color)";
  const value2 = magnitude >= 2 ? 0 : 1 - (magnitude % 1);

  useLayoutEffect(() => {
    const currentSize = Math.min(
      ringRef.current?.offsetHeight || Infinity,
      ringRef.current?.offsetWidth || Infinity,
    );
    if (currentSize !== size) {
      //TODO: Fix rerendering issue here
      //setSize(currentSize);
    }
  }, [height, width, size]);

  return (
    <div ref={ringRef} className={classes.ring} data-testid="Ring">
      <RingProgress
        label={<div className={classes.label}>{label}</div>}
        size={size}
        thickness={8}
        sections={[
          { color: color1, value: value1 * 100 },
          { color: color2, value: value2 * 100 },
        ]}
      />
    </div>
  );
}
