/* eslint-disable @typescript-eslint/no-unused-vars */
import {
  DateTime,
  Duration,
  MarshalMapper,
  baseParameterMarshalers,
  BaseParameterMarshalers,
  baseBodyMarshalers,
  BaseBodyMarshalers,
  baseUnmarshalers,
  BaseUnmarshalers,
} from "./helpers";
/* eslint-enable @typescript-eslint/no-unused-vars */

export type RunStateId = string;

export type TaskDefinitionId = string;

export type PartToId = string;

export type ParameterMarshalers = BaseParameterMarshalers & {
  required: {
    RunStateId: MarshalMapper<RunStateId, string>;

    TaskDefinitionId: MarshalMapper<TaskDefinitionId, string>;

    PartToId: MarshalMapper<PartToId, string>;
  };
};

export const parameterMarshalers: ParameterMarshalers = {
  unrequired: {
    ...baseParameterMarshalers.unrequired,
  },
  required: {
    ...baseParameterMarshalers.required,

    RunStateId: (value: RunStateId) => value,

    TaskDefinitionId: (value: TaskDefinitionId) => value,

    PartToId: (value: PartToId) => value,
  },
};

export type BodyMarshalers = BaseBodyMarshalers & {
  required: {
    RunStateId: MarshalMapper<RunStateId, string>;

    TaskDefinitionId: MarshalMapper<TaskDefinitionId, string>;

    PartToId: MarshalMapper<PartToId, string>;
  };
};

export const bodyMarshalers: BodyMarshalers = {
  unrequired: {
    ...baseBodyMarshalers.unrequired,
  },
  required: {
    ...baseBodyMarshalers.required,

    RunStateId: (value: RunStateId) => value,

    TaskDefinitionId: (value: TaskDefinitionId) => value,

    PartToId: (value: PartToId) => value,
  },
};

export type Unmarshalers = BaseUnmarshalers & {
  required: {
    RunStateId: MarshalMapper<string, RunStateId>;

    TaskDefinitionId: MarshalMapper<string, TaskDefinitionId>;

    PartToId: MarshalMapper<string, PartToId>;
  };
};

export const unmarshalers: Unmarshalers = {
  unrequired: {
    ...baseUnmarshalers.unrequired,
  },
  required: {
    ...baseUnmarshalers.required,

    RunStateId: (value: string) => value,

    TaskDefinitionId: (value: string) => value,

    PartToId: (value: string) => value,
  },
};

export interface PartTo {
  name: string;
  tasks: Array<TaskDefinitionId>;
}

export interface TaskDefinition {
  name: string;
  duration: Duration;
  description: string;
  depends?: Array<string>;
  engagement?: number | undefined;
}

export interface RunState {
  id: RunStateId;
  report: DateTime;
  complete: DateTime;
  duties: Array<TaskDefinitionId>;
  tasks: Array<TaskDefinitionId>;
}
