/* eslint-disable @typescript-eslint/no-unused-vars */
import { PostArgumentsBase, DateTime, Duration, doPost } from "./helpers";

import {
  parameterMarshalers,
  bodyMarshalers,
  unmarshalers,
  PartTo,
  TaskDefinition,
  RunState,
  TaskDefinitionId,
  RunStateId,
  PartToId,
} from "./sharedschemas";
/* eslint-enable @typescript-eslint/no-unused-vars */

export interface RunPostBody {
  jobs: Array<PartToId>;
}

interface WireBody {
  jobs: Array<PartToId>;
}

export interface RunPost200Body {
  id: RunStateId;
  report: DateTime;
  complete: DateTime;
  duties: Array<TaskDefinitionId>;
  tasks: Array<TaskDefinitionId>;
}

interface Wire200Body {
  id: RunStateId;
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
    { jobs: body.jobs.map((value) => bodyMarshalers["PartToId"](value)) },
    {
      200: (body: Wire200Body) => ({
        id: unmarshalers["RunStateId"](body.id),
        report: unmarshalers["date-time"](body.report),
        complete: unmarshalers["date-time"](body.complete),
        duties: body.duties.map((value) =>
          unmarshalers["TaskDefinitionId"](value),
        ),
        tasks: body.tasks.map((value) =>
          unmarshalers["TaskDefinitionId"](value),
        ),
      }),
    },
    {
      200: on200,
    },
  );
