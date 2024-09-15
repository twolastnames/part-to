/* eslint-disable @typescript-eslint/no-unused-vars */
import { Result, DateTime, Duration, useGet } from "./helpers";

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

export interface JobGet200Body {
  id: PartToId;
  name: string;
  tasks: Array<TaskDefinitionId>;
}

interface Wire200Body {
  id: PartToId;
  name: string;
  tasks: Array<TaskDefinitionId>;
}

export interface JobGetArguments {
  id: PartToId;
}

interface ExternalMappers {
  [status: string]: (arg: Wire200Body) => JobGet200Body;

  200: (arg: Wire200Body) => JobGet200Body;
}

export const useJobGet: (args: JobGetArguments) => Result<JobGet200Body> = ({
  id,
}) =>
  useGet<Wire200Body, JobGet200Body, ExternalMappers>(
    "/api/job/",
    [{ name: id, value: parameterMarshalers["PartToId"](id) }],
    {
      200: (body: Wire200Body) => ({
        id: unmarshalers["PartToId"](body.id),
        name: unmarshalers["string"](body.name),
        tasks: body.tasks.map((value) =>
          unmarshalers["TaskDefinitionId"](value),
        ),
      }),
    },
  );
