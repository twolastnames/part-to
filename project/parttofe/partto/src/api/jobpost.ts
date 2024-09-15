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

export interface JobPostBody {
  part_to: { name: string; depends: Array<string> };
  tasks: Array<TaskDefinition>;
}

interface WireBody {
  part_to: { name: string; depends: Array<string> };
  tasks: Array<{
    id: TaskDefinitionId;
    name: string;
    duration: number;
    description: string;
    depends: Array<string>;
    engagement: number;
  }>;
}

export interface JobPost200Body {
  id: PartToId;
  message: string;
}

interface Wire200Body {
  id: PartToId;
  message: string;
}

interface ExternalMappers {
  [status: string]: (arg: Wire200Body) => JobPost200Body;

  200: (arg: Wire200Body) => JobPost200Body;
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
    WireBody,
    Wire200Body,
    JobPost200Body,
    ExternalMappers,
    ExternalHandlers
  >(
    "/api/job/",
    {
      part_to: {
        name: bodyMarshalers["string"](body.part_to.name),
        depends: body.part_to.depends.map((value) =>
          bodyMarshalers["string"](value),
        ),
      },
      tasks: body.tasks.map((value) => ({
        id: bodyMarshalers["TaskDefinitionId"](value.id),
        name: bodyMarshalers["string"](value.name),
        duration: bodyMarshalers["duration"](value.duration),
        description: bodyMarshalers["string"](value.description),
        depends: value.depends.map((value) => bodyMarshalers["string"](value)),
        engagement: bodyMarshalers["number"](value.engagement),
      })),
    },
    {
      200: (body: Wire200Body) => ({
        id: unmarshalers["PartToId"](body.id),
        message: unmarshalers["string"](body.message),
      }),
    },
    {
      200: on200,
    },
  );
