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

export interface ParameterMarshalers extends BaseParameterMarshalers {
  RunStateId: MarshalMapper<RunStateId, string>;

  TaskDefinitionId: MarshalMapper<TaskDefinitionId, string>;

  PartToId: MarshalMapper<PartToId, string>;
}

export const parameterMarshalers: ParameterMarshalers = {
  ...baseParameterMarshalers,

  RunStateId: (value: RunStateId) => value,

  TaskDefinitionId: (value: TaskDefinitionId) => value,

  PartToId: (value: PartToId) => value,
};

export interface BodyMarshalers extends BaseBodyMarshalers {
  RunStateId: MarshalMapper<RunStateId, string>;

  TaskDefinitionId: MarshalMapper<TaskDefinitionId, string>;

  PartToId: MarshalMapper<PartToId, string>;
}

export const bodyMarshalers: BodyMarshalers = {
  ...baseBodyMarshalers,

  RunStateId: (value: RunStateId) => value,

  TaskDefinitionId: (value: TaskDefinitionId) => value,

  PartToId: (value: PartToId) => value,
};

export interface Unmarshalers extends BaseUnmarshalers {
  RunStateId: MarshalMapper<string, RunStateId>;

  TaskDefinitionId: MarshalMapper<string, TaskDefinitionId>;

  PartToId: MarshalMapper<string, PartToId>;
}

export const unmarshalers: Unmarshalers = {
  ...baseUnmarshalers,

  RunStateId: (value: string) => value,

  TaskDefinitionId: (value: string) => value,

  PartToId: (value: string) => value,
};

export interface PartTo {
  id: PartToId;
  name: string;
  tasks: Array<TaskDefinitionId>;
}

export interface TaskDefinition {
  id: TaskDefinitionId;
  name: string;
  duration: Duration;
  description: string;
  depends: Array<string>;
  engagement: number;
}

export interface RunState {
  id: RunStateId;
  report: DateTime;
  complete: DateTime;
  duties: Array<TaskDefinitionId>;
  tasks: Array<TaskDefinitionId>;
}
