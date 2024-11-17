////////////////////////////////////////////////////////////
//  DO NOT DIRECTLY EDIT THIS FILE!!!
//  This file is generated by the updateapi custom django command.
//  Unless functionality needs to be added, the best way to have
//  changes in here is to modify the openapi definition in
//  endpoints.openapi.yaml
////////////////////////////////////////////////////////////

/* eslint-disable @typescript-eslint/no-unused-vars */
import { PostArgumentsBase, doPost } from "./helpers";
import { DateTime } from "../shared/dateTime";
import { Duration } from "../shared/duration";

import {
  parameterMarshalers,
  bodyMarshalers,
  unmarshalers,
  Four04Reply,
  RunOperationReply,
  RunOperation,
  PartTo,
  TaskDefinition,
  RunState,
  PartToId,
  RunStateId,
  TaskDefinitionId,
} from "./sharedschemas";
/* eslint-enable @typescript-eslint/no-unused-vars */

export type RunreportPostBody = { runState?: RunStateId | undefined };

type WireBody = { runState?: RunStateId | undefined };

export type RunreportPost200Body = { runState: RunStateId };

type Wire200Body = { runState: RunStateId };

interface ExternalMappers {
  [status: string]: (arg: Wire200Body) => RunreportPost200Body;

  200: (arg: Wire200Body) => RunreportPost200Body;
}

interface ExternalHandlers {
  [status: string]: (arg: RunreportPost200Body) => void;

  200: (arg: RunreportPost200Body) => void;
}

export interface JobPostArguments extends PostArgumentsBase<RunreportPostBody> {
  on200: (arg: RunreportPost200Body) => void;
}

export const doRunreportPost = async ({
  body,

  on200,
}: JobPostArguments) =>
  await doPost<
    WireBody,
    Wire200Body,
    RunreportPost200Body,
    ExternalMappers,
    ExternalHandlers
  >(
    "/api/run/report",
    { runState: bodyMarshalers.unrequired["RunStateId"](body.runState) },
    {
      200: (body: Wire200Body) => ({
        runState: unmarshalers.required["RunStateId"](body.runState),
      }),
    },
    {
      200: on200,
    },
  );
