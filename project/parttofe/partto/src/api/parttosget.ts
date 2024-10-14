////////////////////////////////////////////////////////////
//  DO NOT DIRECTLY EDIT THIS FILE!!!
//  This file is generated by the updateapi custom django command.
//  Unless functionality needs to be added, the best way to have
//  changes in here is to modify the openapi definition in
//  endpoints.openapi.yaml
////////////////////////////////////////////////////////////

/* eslint-disable @typescript-eslint/no-unused-vars */
import { Result, DateTime, Duration, useGet } from "./helpers";

import {
  parameterMarshalers,
  unmarshalers,
  PartTo,
  TaskDefinition,
  RunState,
  PartToId,
  RunStateId,
  TaskDefinitionId,
} from "./sharedschemas";

/* eslint-enable @typescript-eslint/no-unused-vars */

export interface ParttosGet200Body {
  partTos?: Array<PartToId>;
}

interface Wire200Body {
  partTos?: Array<PartToId>;
}

interface ExternalMappers {
  [status: string]: (arg: Wire200Body) => ParttosGet200Body;

  200: (arg: Wire200Body) => ParttosGet200Body;
}

export type ParttosGetResult = Result<ParttosGet200Body>;

export const useParttosGet: () => ParttosGetResult = () =>
  useGet<Wire200Body, ParttosGet200Body, ExternalMappers>("/api/parttos/", [], {
    200: (body: Wire200Body) => ({
      partTos: body.partTos?.map((value) =>
        unmarshalers.required["PartToId"](value),
      ),
    }),
  });
