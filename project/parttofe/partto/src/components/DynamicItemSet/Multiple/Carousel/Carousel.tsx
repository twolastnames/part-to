import React, { useContext, useEffect, useState } from "react";

import classes from "./Carousel.module.scss";
import { Button } from "../../../Button/Button";
import { Down, Up } from "../../../Icon/Icon";
import { ButtonSet } from "../../ButtonSet/ButtonSet";
import {
  IterationProgress,
  speeds,
} from "../IterationProgress/IterationProgress";
import { Item } from "../../DynamicItemSetTypes";
import { MultipleProps } from "../MultipleTypes";
import { CarouselPage } from "./CarouselTypes";
import { UndefinedDynamicItemSetPair } from "../../../../providers/DynamicItemSetPair";

function getPages(current: Array<Item>) {
  return current.map(({ key, detailView, itemOperations }) => ({
    key,
    view: detailView,
    operations: itemOperations,
  }));
}

export function Carousel({ items, context }: MultipleProps) {
  const [showDuration, setShowDuration] = useState<number>(2);
  const { selected, goForward, goBack } =
    useContext(context.context) || UndefinedDynamicItemSetPair;
  const [paused, setPaused] = useState<boolean>(false);
  const [pages, setPages] = useState<Array<CarouselPage & { key: string }>>(
    getPages(items),
  );

  const itemsLength = items.length;
  context.setCount(itemsLength);
  useEffect(() => {
    if (paused || speeds[showDuration]?.duration == null) {
      return;
    }
    const id = setInterval(
      () => {
        goForward();
      },
      (speeds[showDuration] == null
        ? speeds[2]
        : speeds[showDuration]
      ).duration.toMilliseconds(),
    );
    return () => {
      clearInterval(id);
    };
  }, [showDuration, itemsLength, paused, selected, goForward]);

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
              goBack();
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
              goForward();
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
