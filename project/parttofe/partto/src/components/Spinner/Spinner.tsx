import React, { PropsWithChildren } from "react";

import classes from "./Spinner.module.scss";
import { Result, Stage } from "../../api/helpers";

export interface SpinnerProps<RESPONSE_TYPE> extends PropsWithChildren {
  responses: Array<Result<RESPONSE_TYPE>>;
}

export function willError<RESPONSE_TYPE>(
  responses: Array<Result<RESPONSE_TYPE>>,
) {
  return !!responses.some((response) => response.stage === Stage.Errored);
}

export function willHold<RESPONSE_TYPE>(
  responses: Array<Result<RESPONSE_TYPE>>,
) {
  return (
    !!responses.some((response) =>
      [Stage.Errored, Stage.Fetching, Stage.Skipped].includes(response.stage),
    ) || responses.some((response) => !response?.data)
  );
}

export function Spinner<RESPONSE_TYPE>({
  responses,
  children,
}: SpinnerProps<RESPONSE_TYPE>) {
  if (willError(responses)) {
    return (
      <div className={classes.error} data-testid="Spinner">
        {`Page Load Error: ${
          responses.find((response) => response?.stage === Stage.Errored)
            ?.status
        }`}
      </div>
    );
  }
  if (willHold(responses)) {
    return (
      <div className={classes.error} data-testid="Spinner">
        Loading...
      </div>
    );
  }
  return <> {children} </>;
}
