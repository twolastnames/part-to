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
  PartTo,
  TaskDefinition,
  RunState,
  RunStateId,
  TaskDefinitionId,
  PartToId,
} from "./sharedschemas";
/* eslint-enable @typescript-eslint/no-unused-vars */

export interface RunPostBody {
  partTo: Array<PartToId>;
}

interface WireBody {
  partTo: Array<PartToId>;
}

export interface RunPost200Body {
  runState: RunStateId;
  report: DateTime;
  complete: DateTime;
  duties: Array<TaskDefinitionId>;
  tasks: Array<TaskDefinitionId>;
}

interface Wire200Body {
  runState: RunStateId;
  report: string;
  complete: string;
  duties: Array<TaskDefinitionId>;
  tasks: Array<TaskDefinitionId>;
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
      partTo: body.partTo.map((value) =>
        bodyMarshalers.required["PartToId"](value),
      ),
    },
    {
      200: (body: Wire200Body) => ({
        runState: unmarshalers.required["RunStateId"](body.runState),
        report: unmarshalers.required["date-time"](body.report),
        complete: unmarshalers.required["date-time"](body.complete),
        duties: body.duties.map((value) =>
          unmarshalers.required["TaskDefinitionId"](value),
        ),
        tasks: body.tasks.map((value) =>
          unmarshalers.required["TaskDefinitionId"](value),
        ),
      }),
    },
    {
      200: on200,
    },
  );
