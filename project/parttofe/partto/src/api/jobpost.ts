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

export interface JobPostBody {
  part_to: { name: string; depends: Array<UUID> };
  tasks: Array<Task>;
}

interface JobPostWireBody {
  part_to: { name: string; depends: Array<string> };
  tasks: Array<{
    name: string;
    duration: number;
    description: string;
    depends: Array<string>;
    engagement: number;
  }>;
}

export interface JobPost200Body {
  id: UUID;
  message: string;
}

interface JobPost200WireBody {
  id: string;
  message: string;
}

interface ExternalMappers {
  [status: string]: (arg: JobPost200WireBody) => JobPost200Body;

  200: (arg: JobPost200WireBody) => JobPost200Body;
}

interface ExternalHandlers {
  [status: string]: (arg: JobPost200Body) => void;

  200: (arg: JobPost200Body) => void;
}

export interface JobPostArguments extends PostArgumentsBase<JobPostBody> {
  on200: (arg: JobPost200Body) => void;
}

export const doJobPost = async ({
  body,

  on200,
}: JobPostArguments) =>
  await doPost<
    JobPostWireBody,
    JobPost200WireBody,
    JobPost200Body,
    ExternalMappers,
    ExternalHandlers
  >(
    "/api/job/",
    {
      part_to: {
        name: unmarshalers["string"](body.part_to.name),
        depends: body.part_to.depends.map((value) =>
          unmarshalers["uuid"](value),
        ),
      },
      tasks: body.tasks.map((value) => ({
        name: unmarshalers["string"](value.name),
        duration: unmarshalers["duration"](value.duration),
        description: unmarshalers["string"](value.description),
        depends: value.depends.map((value) => unmarshalers["string"](value)),
        engagement: unmarshalers["number"](value.engagement),
      })),
    },
    {
      200: (body: JobPost200WireBody) => ({
        id: unmarshalers["uuid"](body.id),
        message: unmarshalers["string"](body.message),
      }),
    },
    {
      200: on200,
    },
  );
