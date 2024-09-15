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

export type TaskDefinitionId = string;

export type RunStateId = string;

export type PartToId = string;

export interface ParameterMarshalers extends BaseParameterMarshalers {
  TaskDefinitionId: MarshalMapper<TaskDefinitionId, string>;

  RunStateId: MarshalMapper<RunStateId, string>;

  PartToId: MarshalMapper<PartToId, string>;
}

export const parameterMarshalers: ParameterMarshalers = {
  ...baseParameterMarshalers,

  TaskDefinitionId: (value: TaskDefinitionId) => value,

  RunStateId: (value: RunStateId) => value,

  PartToId: (value: PartToId) => value,
};

export interface BodyMarshalers extends BaseBodyMarshalers {
  TaskDefinitionId: MarshalMapper<TaskDefinitionId, string>;

  RunStateId: MarshalMapper<RunStateId, string>;

  PartToId: MarshalMapper<PartToId, string>;
}

export const bodyMarshalers: BodyMarshalers = {
  ...baseBodyMarshalers,

  TaskDefinitionId: (value: TaskDefinitionId) => value,

  RunStateId: (value: RunStateId) => value,

  PartToId: (value: PartToId) => value,
};

export interface Unmarshalers extends BaseUnmarshalers {
  TaskDefinitionId: MarshalMapper<string, TaskDefinitionId>;

  RunStateId: MarshalMapper<string, RunStateId>;

  PartToId: MarshalMapper<string, PartToId>;
}

export const unmarshalers: Unmarshalers = {
  ...baseUnmarshalers,

  TaskDefinitionId: (value: string) => value,

  RunStateId: (value: string) => value,

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
