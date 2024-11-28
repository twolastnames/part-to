import React from "react";

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
        Loading...
      </div>
    );
  }
  return <> {children} </>;
}
