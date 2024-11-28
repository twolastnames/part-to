import { PropsWithChildren } from "react";
import { Stage } from "../../api/helpers";

export type ResponseStatusCheckable = {
  stage: Stage;
  status?: number;
};

export interface SpinnerProps extends PropsWithChildren {
  responses: Array<ResponseStatusCheckable>;
}
