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

export type PartToId = string;

export type RunStateId = string;

export type TaskDefinitionId = string;

export type ParameterMarshalers = BaseParameterMarshalers & {
  required: {
    PartToId: MarshalMapper<PartToId, string>;

    RunStateId: MarshalMapper<RunStateId, string>;

    TaskDefinitionId: MarshalMapper<TaskDefinitionId, string>;
  };
};

export const parameterMarshalers: ParameterMarshalers = {
  unrequired: {
    ...baseParameterMarshalers.unrequired,
  },
  required: {
    ...baseParameterMarshalers.required,

    PartToId: (value: PartToId) => value,

    RunStateId: (value: RunStateId) => value,

    TaskDefinitionId: (value: TaskDefinitionId) => value,
  },
};

export type BodyMarshalers = BaseBodyMarshalers & {
  required: {
    PartToId: MarshalMapper<PartToId, string>;

    RunStateId: MarshalMapper<RunStateId, string>;

    TaskDefinitionId: MarshalMapper<TaskDefinitionId, string>;
  };
};

export const bodyMarshalers: BodyMarshalers = {
  unrequired: {
    ...baseBodyMarshalers.unrequired,
  },
  required: {
    ...baseBodyMarshalers.required,

    PartToId: (value: PartToId) => value,

    RunStateId: (value: RunStateId) => value,

    TaskDefinitionId: (value: TaskDefinitionId) => value,
  },
};

export type Unmarshalers = BaseUnmarshalers & {
  required: {
    PartToId: MarshalMapper<string, PartToId>;

    RunStateId: MarshalMapper<string, RunStateId>;

    TaskDefinitionId: MarshalMapper<string, TaskDefinitionId>;
  };
};

export const unmarshalers: Unmarshalers = {
  unrequired: {
    ...baseUnmarshalers.unrequired,
  },
  required: {
    ...baseUnmarshalers.required,

    PartToId: (value: string) => value,

    RunStateId: (value: string) => value,

    TaskDefinitionId: (value: string) => value,
  },
};

export interface PartTo {
  name: string;
  workDuration?: Duration | undefined;
  clockDuration?: Duration | undefined;
  tasks: Array<TaskDefinitionId>;
}

export interface TaskDefinition {
  duration: Duration;
  description: string;
  depends?: Array<TaskDefinitionId>;
  engagement?: number | undefined;
}

export interface RunState {
  runState: RunStateId;
  report: DateTime;
  complete: DateTime;
  duties: Array<TaskDefinitionId>;
  tasks: Array<TaskDefinitionId>;
}
