import React, { useEffect, useState } from "react";

import classes from "./Carousel.module.scss";
import { Button } from "../../../Button/Button";
import { Down, Up } from "../../../Icon/Icon";
import { ButtonSet } from "../../ButtonSet/ButtonSet";
import { IterationProgress } from "../IterationProgress/IterationProgress";
import { Item } from "../../DynamicItemSetTypes";
import { MultipleProps } from "../MultipleTypes";
import { CarouselPage } from "./CarouselTypes";
import { useSingleOfPair } from "../../../../providers/DynamicItemSetPair";

function getPages(current: Array<Item>) {
  return current.map(({ key, detailView, itemOperations }) => ({
    key,
    view: detailView,
    operations: itemOperations,
  }));
}

export function Carousel({ items, context, pausedByDefault }: MultipleProps) {
  const [initialized, setInitialized] = useState<boolean>(false);
  const { paused, togglePause, selected, goForward, goBack, showDuration } =
    useSingleOfPair(context);
  const [pages, setPages] = useState<Array<CarouselPage & { key: string }>>(
    getPages(items),
  );
  useEffect(() => {
    if (!initialized) {
      if ((!paused && pausedByDefault) || (paused && !pausedByDefault)) {
        togglePause();
      }
      setInitialized(true);
    }
  }, [paused, initialized, pausedByDefault, togglePause]);

  const itemsLength = items.length;
  context.setCount(itemsLength);
  useEffect(() => {
    if (paused) {
      return;
    }
    const id = setInterval(() => {
      goForward();
    }, showDuration.toMilliseconds());
    return () => {
      clearInterval(id);
    };
  }, [showDuration, paused, goForward]);

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
      <IterationProgress context={context} />
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
