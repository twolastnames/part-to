/* eslint-disable @typescript-eslint/no-unused-vars */
import {
  PostArgumentsBase,
  UUID,
  DateTime,
  Duration,
  doPost,
  bodyMarshalers,
  unmarshalers,
} from "./helpers";

import { Task, RunState } from "./sharedschemas";
/* eslint-enable @typescript-eslint/no-unused-vars */

export interface RunPostBody {
  jobs: Array<UUID>;
}

interface RunPostWireBody {
  jobs: Array<string>;
}

export interface RunPost200Body {
  id: UUID;
  report: DateTime;
  complete: DateTime;
  duties: Array<UUID>;
  tasks: Array<UUID>;
}

interface RunPost200WireBody {
  id: string;
  report: string;
  complete: string;
  duties: Array<string>;
  tasks: Array<string>;
}

interface ExternalMappers {
  [status: string]: (arg: RunPost200WireBody) => RunPost200Body;

  200: (arg: RunPost200WireBody) => RunPost200Body;
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
    RunPostWireBody,
    RunPost200WireBody,
    RunPost200Body,
    ExternalMappers,
    ExternalHandlers
  >(
    "/api/run/",
    { jobs: body.jobs.map((value) => unmarshalers["uuid"](value)) },
    {
      200: (body: RunPost200WireBody) => ({
        id: unmarshalers["uuid"](body.id),
        report: unmarshalers["date-time"](body.report),
        complete: unmarshalers["date-time"](body.complete),
        duties: body.duties.map((value) => unmarshalers["uuid"](value)),
        tasks: body.tasks.map((value) => unmarshalers["uuid"](value)),
      }),
    },
    {
      200: on200,
    },
  );
