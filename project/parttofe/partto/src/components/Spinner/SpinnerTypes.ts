import { PropsWithChildren } from "react";
import { Result } from "../../api/helpers";

export interface SpinnerProps<RESPONSE_TYPE> extends PropsWithChildren {
  responses: Array<Result<RESPONSE_TYPE>>;
}
