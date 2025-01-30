import React, { useEffect, useState } from "react";

import classes from "./Spinner.module.scss";
import { Stage } from "../../api/helpers";
import { Error } from "../Error/Error";
import { ResponseStatusCheckable, SpinnerProps } from "./SpinnerTypes";

export function willError(responses: Array<ResponseStatusCheckable>) {
  return !!responses.some((response) => response.stage === Stage.Errored);
}

export function willHold(responses: Array<ResponseStatusCheckable>) {
  return !!responses.some((response) =>
    [Stage.Errored, Stage.Fetching, Stage.Skipped].includes(response.stage),
  );
}

function DelayedText() {
  const [text, setText] = useState<string>("");
  useEffect(() => {
    const id = setTimeout(() => {
      setText("Loading...");
    }, 500);
    return () => {
      clearTimeout(id);
    };
  });
  return <>{text}</>;
}

export function Spinner({ responses, children }: SpinnerProps) {
  if (willError(responses || [])) {
    return (
      <div className={classes.error} data-testid="Spinner">
        <Error
          code={Number(
            (responses || []).find(
              (response) => response?.stage === Stage.Errored,
            )?.status || 0,
          )}
        />
      </div>
    );
  }
  if (willHold(responses || [])) {
    return (
      <div className={classes.error} data-testid="Spinner">
        <DelayedText />
      </div>
    );
  }
  return <> {children} </>;
}
