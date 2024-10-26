////////////////////////////////////////////////////////////
//  DO NOT DIRECTLY EDIT THIS FILE!!!
//  This file is generated by the updateapi custom django command.
//  Unless functionality needs to be added, the best way to have
//  changes in here is to modify the openapi definition in
//  endpoints.openapi.yaml
////////////////////////////////////////////////////////////

/* eslint-disable @typescript-eslint/no-unused-vars */
import { PostArgumentsBase, DateTime, Duration, doPost } from "./helpers";

import {
  parameterMarshalers,
  bodyMarshalers,
  unmarshalers,
  RunOperation,
  PartTo,
  TaskDefinition,
  RunState,
  PartToId,
  RunStateId,
  TaskDefinitionId,
} from "./sharedschemas";
/* eslint-enable @typescript-eslint/no-unused-vars */

export interface RunPostBody {
  runState?: RunStateId | undefined;
  operations?: Array<RunOperation>;
}

interface WireBody {
  runState?: RunStateId | undefined;
  operations?: Array<{ task: TaskDefinitionId; operation: string }>;
}

export interface RunPost200Body {
  runState: RunStateId;
}

interface Wire200Body {
  runState: RunStateId;
}

interface ExternalMappers {
  [status: string]: (arg: Wire200Body) => RunPost200Body;

  200: (arg: Wire200Body) => RunPost200Body;
}

interface ExternalHandlers {
  [status: string]: (arg: RunPost200Body) => void;

  200: (arg: RunPost200Body) => void;
}

export interface JobPostArguments extends PostArgumentsBase<RunPostBody> {
  on200: (arg: RunPost200Body) => void;
}

export const doRunPost = async ({
  body,

  on200,
}: JobPostArguments) =>
  await doPost<
    WireBody,
    Wire200Body,
    RunPost200Body,
    ExternalMappers,
    ExternalHandlers
  >(
    "/api/run/",
    {
      runState: bodyMarshalers.unrequired["RunStateId"](body.runState),
      operations: body.operations?.map((value) => ({
        task: bodyMarshalers.required["TaskDefinitionId"](value.task),
        operation: bodyMarshalers.required["string"](value.operation),
      })),
    },
    {
      200: (body: Wire200Body) => ({
        runState: unmarshalers.required["RunStateId"](body.runState),
      }),
    },
    {
      200: on200,
    },
  );
