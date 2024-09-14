/* eslint-disable @typescript-eslint/no-unused-vars */
import {
  Result,
  UUID,
  DateTime,
  Duration,
  parameterMarshalers,
  unmarshalers,
  useGet,
} from "./helpers";
/* eslint-enable @typescript-eslint/no-unused-vars */

export interface JobGet200Body {
  id: UUID;
  name: string;
  tasks: Array<UUID>;
}

interface JobGet200WireBody {
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

export const useJobGet: (args: JobGetArguments) => Result<JobGet200Body> = ({
  id,
}) =>
  useGet<JobGet200WireBody, JobGet200Body, JobGetExternalMappers>(
    "/api/job/",
    [{ name: id, value: parameterMarshalers["uuid"](id) }],
    {
      200: (body: JobGet200WireBody) => ({
        id: unmarshalers["uuid"](body.id),
        name: unmarshalers["string"](body.name),
        tasks: body.tasks.map((value) => unmarshalers["uuid"](value)),
      }),
    },
  );
