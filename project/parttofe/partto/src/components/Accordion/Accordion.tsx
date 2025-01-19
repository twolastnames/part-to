import React from "react";

import classes from "./Accordion.module.scss";
import { AccordionProps } from "./AccordionTypes";

export function Accordion({ summary, children }: AccordionProps) {
  return (
    <details className={classes.accordion} open={true} data-testid="Accordion">
      <summary>{summary}</summary>
      <div className={classes.body}>{children}</div>
    </details>
  );
}
