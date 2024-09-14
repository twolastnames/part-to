import {
  Result,
  UUID,
  parameterMarshalers,
  unmarshalers,
  useGet,
} from "./helpers";

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
  id: UUID;
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
