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
  unrequired: {
    PartToId: MarshalMapper<PartToId | undefined, string | undefined>;

    RunStateId: MarshalMapper<RunStateId | undefined, string | undefined>;

    TaskDefinitionId: MarshalMapper<
      TaskDefinitionId | undefined,
      string | undefined
    >;
  };
};

export const parameterMarshalers: ParameterMarshalers = {
  unrequired: {
    ...baseParameterMarshalers.unrequired,

    PartToId: (value?: PartToId) => value,

    RunStateId: (value?: RunStateId) => value,

    TaskDefinitionId: (value?: TaskDefinitionId) => value,
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
  unrequired: {
    PartToId: MarshalMapper<PartToId | undefined, string | undefined>;

    RunStateId: MarshalMapper<RunStateId | undefined, string | undefined>;

    TaskDefinitionId: MarshalMapper<
      TaskDefinitionId | undefined,
      string | undefined
    >;
  };
};

export const bodyMarshalers: BodyMarshalers = {
  unrequired: {
    ...baseBodyMarshalers.unrequired,

    PartToId: (value?: PartToId) => value,

    RunStateId: (value?: RunStateId) => value,

    TaskDefinitionId: (value?: TaskDefinitionId) => value,
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
  unrequired: {
    PartToId: MarshalMapper<string | undefined, PartToId | undefined>;

    RunStateId: MarshalMapper<string | undefined, RunStateId | undefined>;

    TaskDefinitionId: MarshalMapper<
      string | undefined,
      TaskDefinitionId | undefined
    >;
  };
};

export const unmarshalers: Unmarshalers = {
  unrequired: {
    ...baseUnmarshalers.unrequired,

    PartToId: (value?: string) => value,

    RunStateId: (value?: string) => value,

    TaskDefinitionId: (value?: string) => value,
  },
  required: {
    ...baseUnmarshalers.required,

    PartToId: (value: string) => value,

    RunStateId: (value: string) => value,

    TaskDefinitionId: (value: string) => value,
  },
};

export interface Four04Reply {
  messages?: Array<string>;
}

export interface RunOperationReply {
  runState: RunStateId;
}

export interface RunOperation {
  runState?: RunStateId | undefined;
  definitions: Array<TaskDefinitionId>;
}

export interface PartTo {
  name: string;
  workDuration?: Duration | undefined;
  clockDuration?: Duration | undefined;
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
  runState: RunStateId;
  report?: DateTime | undefined;
  complete?: DateTime | undefined;
  activePartTos?: Array<PartToId>;
  staged: Array<TaskDefinitionId>;
  started: Array<TaskDefinitionId>;
  created: Array<TaskDefinitionId>;
  voided: Array<TaskDefinitionId>;
  completed: Array<TaskDefinitionId>;
}
