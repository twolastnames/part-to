import React, { ReactNode, useEffect, useState } from "react";

import classes from "./Carousel.module.scss";
import { Button, ButtonProps } from "../../../Button/Button";
import { Down, Up } from "../../../Icon/Icon";
import { ButtonSet } from "../../ButtonSet/ButtonSet";
import {
  IterationProgress,
  speeds,
} from "../IterationProgress/IterationProgress";
import { MultipleProps } from "../Multiple";
import { Item } from "../../DynamicItemSet";

export type CarouselPage = { view: ReactNode; operations?: Array<ButtonProps> };

type GoADirection = (
  totalPages: number,
  setSelected: (mutator: (arg: number) => number) => void,
) => void;

const goBack: GoADirection = (length, setSelected) => {
  setSelected((last: number) => (last <= 0 ? length - 1 : last - 1));
};
const goForward: GoADirection = (length, setSelected) => {
  setSelected((last: number) => (last >= length - 1 ? 0 : last + 1));
};

function getPages(current: Array<Item>) {
  return current.map(({ key, detailView, itemOperations }) => ({
    key,
    view: detailView,
    operations: itemOperations,
  }));
}

export function Carousel({ items }: MultipleProps) {
  const [showDuration, setShowDuration] = useState<number>(2);
  const [selected, setSelected] = useState<number>(0);
  const [paused, setPaused] = useState<boolean>(false);
  const [pages, setPages] = useState<Array<CarouselPage & { key: string }>>(
    getPages(items),
  );

  const itemsLength = items.length;
  useEffect(() => {
    if (paused || speeds[showDuration]?.duration == null) {
      return;
    }
    const id = setInterval(
      () => {
        goForward(itemsLength, setSelected);
      },
      (speeds[showDuration] == null
        ? speeds[2]
        : speeds[showDuration]
      ).duration.toMilliseconds(),
    );
    return () => {
      clearInterval(id);
    };
  }, [showDuration, itemsLength, paused, selected]);

  useEffect(() => {
    setPages(getPages(items));
  }, [items]);

  const operations = pages[selected]?.operations;
  return (
    <div
      key={pages[selected]?.key}
      className={classes.multiple}
      data-testid="Carousel"
    >
      <div className={classes.carousel}>
        <div className={classes.carouselButton}>
          <Button
            icon={Up}
            text="Back One"
            onClick={() => {
              goBack(pages.length, setSelected);
            }}
          />
        </div>
        <div className={classes.content}>
          <div key={pages[selected]?.key} className={classes.listView}>
            {pages[selected]?.view}
          </div>
        </div>
        <div className={classes.carouselButton}>
          <Button
            icon={Down}
            text="Forward One"
            onClick={() => {
              goForward(pages.length, setSelected);
            }}
          />
        </div>
      </div>
      <IterationProgress
        setShowDuration={setShowDuration}
        on={selected}
        total={pages.length}
        showDuration={showDuration}
        setPaused={setPaused}
        paused={paused}
      />
      {operations ? (
        <div className={classes.buttonSet}>
          <div className={classes.buttons}>
            <ButtonSet operations={operations} />
          </div>
        </div>
      ) : (
        <></>
      )}
    </div>
  );
}
