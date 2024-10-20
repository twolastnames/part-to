////////////////////////////////////////////////////////////
//  DO NOT DIRECTLY EDIT THIS FILE!!!
//  This file is generated by the updateapi custom django command.
//  Unless functionality needs to be added, the best way to have
//  changes in here is to modify the openapi definition in
//  endpoints.openapi.yaml
////////////////////////////////////////////////////////////

/* eslint-disable @typescript-eslint/no-unused-vars */
import { PostArgumentsBase, DateTime, Duration, doPost } from "./helpers";

import {
  parameterMarshalers,
  bodyMarshalers,
  unmarshalers,
  PartTo,
  TaskDefinition,
  RunState,
  PartToId,
  RunStateId,
  TaskDefinitionId,
} from "./sharedschemas";
/* eslint-enable @typescript-eslint/no-unused-vars */

export interface ParttoPostBody {
  part_to: { name: string; depends: Array<string> };
  tasks: Array<TaskDefinition>;
}

interface WireBody {
  part_to: { name: string; depends: Array<string> };
  tasks: Array<{
    duration: number;
    description: string;
    depends?: Array<TaskDefinitionId>;
    engagement?: number | undefined;
  }>;
}

export interface ParttoPost200Body {
  partTo: PartToId;
  message: string;
}

interface Wire200Body {
  partTo: PartToId;
  message: string;
}

interface ExternalMappers {
  [status: string]: (arg: Wire200Body) => ParttoPost200Body;

  200: (arg: Wire200Body) => ParttoPost200Body;
}

interface ExternalHandlers {
  [status: string]: (arg: ParttoPost200Body) => void;

  200: (arg: ParttoPost200Body) => void;
}

export interface JobPostArguments extends PostArgumentsBase<ParttoPostBody> {
  on200: (arg: ParttoPost200Body) => void;
}

export const doParttoPost = async ({
  body,

  on200,
}: JobPostArguments) =>
  await doPost<
    WireBody,
    Wire200Body,
    ParttoPost200Body,
    ExternalMappers,
    ExternalHandlers
  >(
    "/api/task/",
    {
      part_to: {
        name: bodyMarshalers.required["string"](body.part_to.name),
        depends: body.part_to.depends.map((value) =>
          bodyMarshalers.required["string"](value),
        ),
      },
      tasks: body.tasks.map((value) => ({
        duration: bodyMarshalers.required["duration"](value.duration),
        description: bodyMarshalers.required["string"](value.description),
        depends: value.depends?.map((value) =>
          bodyMarshalers.required["TaskDefinitionId"](value),
        ),
        engagement: bodyMarshalers.unrequired["number"](value.engagement),
      })),
    },
    {
      200: (body: Wire200Body) => ({
        partTo: unmarshalers.required["PartToId"](body.partTo),
        message: unmarshalers.required["string"](body.message),
      }),
    },
    {
      200: on200,
    },
  );
