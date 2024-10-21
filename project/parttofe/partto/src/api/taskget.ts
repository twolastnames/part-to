////////////////////////////////////////////////////////////
//  DO NOT DIRECTLY EDIT THIS FILE!!!
//  This file is generated by the updateapi custom django command.
//  Unless functionality needs to be added, the best way to have
//  changes in here is to modify the openapi definition in
//  endpoints.openapi.yaml
////////////////////////////////////////////////////////////

/* eslint-disable @typescript-eslint/no-unused-vars */
import { Result, DateTime, Duration, useGet } from "./helpers";

import {
  parameterMarshalers,
  unmarshalers,
  PartTo,
  TaskDefinition,
  RunState,
  PartToId,
  RunStateId,
  TaskDefinitionId,
} from "./sharedschemas";

/* eslint-enable @typescript-eslint/no-unused-vars */

export interface TaskGet200Body {
  duration: Duration;
  description: string;
  depends?: Array<TaskDefinitionId>;
  engagement?: number | undefined;
}

interface Wire200Body {
  duration: number;
  description: string;
  depends?: Array<TaskDefinitionId>;
  engagement?: number | undefined;
}

export interface TaskGetArguments {
  task: TaskDefinitionId;
}

interface ExternalMappers {
  [status: string]: (arg: Wire200Body) => TaskGet200Body;

  200: (arg: Wire200Body) => TaskGet200Body;
}

export type TaskGetResult = Result<TaskGet200Body>;

export const useTaskGet: (args: TaskGetArguments) => TaskGetResult = ({
  task,
}) =>
  useGet<Wire200Body, TaskGet200Body, ExternalMappers>(
    "/api/task/",
    [
      {
        name: "task",
        value: parameterMarshalers.required["TaskDefinitionId"](task),
      },
    ],
    {
      200: (body: Wire200Body) => ({
        duration: unmarshalers.required["duration"](body.duration),
        description: unmarshalers.required["string"](body.description),
        depends: body.depends?.map((value) =>
          unmarshalers.required["TaskDefinitionId"](value),
        ),
        engagement: unmarshalers.unrequired["number"](body.engagement),
      }),
    },
  );
