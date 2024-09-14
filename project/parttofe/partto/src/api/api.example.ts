import {
  PostArgumentsBase,
  Result,
  UUID,
  doPost,
  bodyMarshalers,
  parameterMarshalers,
  unmarshalers,
  useGet,
} from "./helpers";

export interface Task {
  name: string;
  duration: number; //milliseconds
  description: string;
  depends?: Array<string>;
  engagement: number;
}

export interface WireTask {
  name: string;
  duration: number; //milliseconds
  description: string;
  depends?: Array<string>;
  engagement: number;
}

export interface JobGet200Body {
  id: UUID;
  name: string;
  tasks: Array<UUID>;
}

export interface JobGet200WireBody {
  id: string;
  name: string;
  tasks: Array<string>;
}

export interface JobGetArguments {
  id: string;
}

interface JobGetExternalMappers {
  [status: string]: (arg: JobGet200WireBody) => JobGet200Body;
  200: (arg: JobGet200WireBody) => JobGet200Body;
}

export type JobGetResultType = Result<JobGet200Body>;

export const useJobGet: (args: JobGetArguments) => Result<JobGet200Body> = ({
  id,
}) =>
  useGet<JobGet200WireBody, JobGet200Body, JobGetExternalMappers>(
    "/api/job/",
    [{ name: "id", value: parameterMarshalers["uuid"](id) }],
    {
      200: (body: JobGet200WireBody) => ({
        id: unmarshalers["uuid"](body.id),
        name: unmarshalers["string"](body.name),
        tasks: body.tasks.map(unmarshalers["uuid"]),
      }),
    },
  );

export interface JobPostBody {
  part_to: { name: string; depends: Array<string> };
  tasks: Array<Task>;
}

interface JobPostWireBody {
  part_to: { name: string; depends: Array<string> };
  tasks: Array<Task>;
}

export interface JobPost200WireBody {
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

export interface RunPostBody {
  jobs: Array<UUID>;
}

interface RunPostWireBody {
  jobs: Array<string>;
}

export interface RunPost200Body {
  id: UUID;
  report: Date;
  complete: Date;
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

type RunPost200ExternalHandler = (arg: RunPost200Body) => void;

export interface RunPostArguments extends PostArgumentsBase<RunPostBody> {
  on200: RunPost200ExternalHandler;
}

interface RunPostExternalMappers {
  [status: string]: (arg: RunPost200WireBody) => RunPost200Body;
  200: (arg: RunPost200WireBody) => RunPost200Body;
}

interface RunPostExternalHandlers {
  [staus: string]: RunPost200ExternalHandler;
  200: RunPost200ExternalHandler;
}

export const doRunPost = async ({ body, on200 }: RunPostArguments) =>
  doPost<
    RunPostWireBody,
    RunPost200WireBody,
    RunPost200Body,
    RunPostExternalMappers,
    RunPostExternalHandlers
  >(
    "/some/endpoint",
    {
      jobs: body.jobs.map(bodyMarshalers["uuid"]),
    },
    {
      200: (body: RunPost200WireBody) => ({
        id: unmarshalers["string"](body.id),
        report: unmarshalers["date-time"](body.report),
        complete: unmarshalers["date-time"](body.complete),
        duties: (body.duties || []).map(unmarshalers["uuid"]),
        tasks: (body.tasks || []).map(unmarshalers["uuid"]),
      }),
    },
    {
      200: on200,
    },
  );
