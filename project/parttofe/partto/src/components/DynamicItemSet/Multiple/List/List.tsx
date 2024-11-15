import React, {
  PropsWithChildren,
  useLayoutEffect,
  useRef,
  useState,
} from "react";

import { Carousel } from "../Carousel/Carousel";
import { ButtonProps } from "../../../Button/ButtonTypes";
import { MultipleProps } from "../MultipleTypes";

interface ShellProps extends PropsWithChildren {
  height: number;
  operations: Array<ButtonProps>;
}

function Shell({ children, height, operations }: ShellProps) {
  return <div style={{ height }}>{children}</div>;
}

export function List({ items }: MultipleProps) {
  const minimumHeight = 120;
  const domRef = useRef<HTMLDivElement>(null);
  const [{ height, perPage }, setCalculated] = useState<{
    height: number;
    perPage: number;
  }>({ height: 0, perPage: 0 });

  const calculateHeight = () => {
    if (!domRef.current) {
      return;
    }
    const { height: rectangleHeight } =
      domRef?.current?.getBoundingClientRect();
    const screenHeight = rectangleHeight;
    const count = Math.floor(screenHeight / minimumHeight);
    const height = Math.floor(screenHeight / count);

    setCalculated({
      height,
      perPage: count === 0 ? 1 : count,
    });
  };

  useLayoutEffect(() => {
    calculateHeight();
  }, [domRef]);

  const pages = [];
  if (height > 0) {
    for (let index = 0; index < items.length; index += perPage) {
      pages.push({
        view: (
          <div key={index}>
            {items.slice(index, index + perPage).map((item, key) => (
              <Shell
                key={`${index}-${key}`}
                height={height}
                operations={item.itemOperations}
              >
                {item.listView}
              </Shell>
            ))}
          </div>
        ),
      });
    }
  }

  return (
    <div data-testid="List" style={{ height: "100%" }} ref={domRef}>
      {items.length > 0 ? <Carousel items={items} /> : null}
    </div>
  );
}
