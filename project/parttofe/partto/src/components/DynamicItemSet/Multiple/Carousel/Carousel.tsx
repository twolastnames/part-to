import React, { ReactNode, useEffect, useState } from "react";

import classes from "./Carousel.module.scss";
import { Button, ButtonProps } from "../../../Button/Button";
import { Down, Up } from "../../../Icon/Icon";
import { ButtonSet } from "../../ButtonSet/ButtonSet";
import {
  IterationProgress,
  marks,
} from "../IterationProgress/IterationProgress";

export type CarouselPage = { view: ReactNode; operations?: Array<ButtonProps> };

export interface CarouselProps {
  pages: Array<CarouselPage>;
}

type GoADirection = (
  totalPages: number,
  setSelected: (mutator: (arg: number) => number) => void,
) => void;

const goBack: GoADirection = (length, setSelected) => {
  setSelected((last: number) => (last <= 0 ? length - 1 : last - 1));
};
const goForward: GoADirection = (length, setSelected) => {
  setSelected((last) => (last >= length - 1 ? 0 : last + 1));
};

export function Carousel({ pages }: CarouselProps) {
  const [showDuration, setShowDuration] = useState<number>(2);
  const [selected, setSelected] = useState<number>(0);
  useEffect(() => {
    if (marks[showDuration]?.duration == null) {
      return;
    }
    const id = setInterval(
      () => {
        goForward(pages.length, setSelected);
      },
      (marks[showDuration] == null
        ? marks[2]
        : marks[showDuration]
      ).duration.toMilliseconds(),
    );
    return () => {
      clearInterval(id);
    };
  }, [showDuration, pages.length]);
  const operations = pages[selected]?.operations;
  return (
    <div key={selected} className={classes.multiple} data-testid="Carousel">
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
          <div className={classes.listView}>{pages[selected].view}</div>
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
