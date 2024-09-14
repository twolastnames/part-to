import {
  PostArgumentsBase,
  UUID,
  doPost,
  bodyMarshalers,
  unmarshalers,
} from "./helpers";

import { Task } from "./sharedschemas.example";

interface TaskWire {
  name: string;
  duration: string;
  description: string;
  depends: Array<string>;
  engagement: number;
}

export interface JobPostBody {
  part_to: { name: string; depends: Array<string> };
  tasks: Array<Task>;
}

interface JobPostWireBody {
  part_to: { name: string; depends: Array<string> };
  tasks: Array<TaskWire>;
}

interface JobPost200WireBody {
  id: string;
}

export interface JobPost200Body {
  id: UUID;
}

export interface JobPostArguments extends PostArgumentsBase<JobPostBody> {
  on200: (arg: JobPost200Body) => void;
}

interface JobPostExternalMappers {
  [status: string]: (arg: JobPost200WireBody) => JobPost200Body;
  200: (arg: JobPost200WireBody) => JobPost200Body;
}

interface JobPostExternalHandlers {
  [staus: string]: (arg: JobPost200Body) => void;
  200: (arg: JobPost200Body) => void;
}

export const doJobPost = async ({ body, on200 }: JobPostArguments) =>
  await doPost<
    JobPostWireBody,
    JobPost200WireBody,
    JobPost200Body,
    JobPostExternalMappers,
    JobPostExternalHandlers
  >(
    "/api/job/",
    {
      part_to: {
        name: bodyMarshalers["string"](body.part_to.name),
        depends: body.part_to.depends.map(bodyMarshalers["string"]),
      },
      tasks: body.tasks.map(
        ({ name, duration, description, depends, engagement }: Task) => ({
          name: bodyMarshalers.string(name),
          description: bodyMarshalers.string(description),
          duration: bodyMarshalers.number(duration),
          depends: depends ? depends.map(bodyMarshalers.string) : undefined,
          engagement: bodyMarshalers.number(engagement),
        }),
      ),
    },
    {
      200: (body: JobPost200WireBody) => ({
        id: unmarshalers.uuid(body.id),
      }),
    },
    {
      200: on200,
    },
  );
