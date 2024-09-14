import { useEffect, useState } from "react";

export const unmarshalUuid = (value: string) => {
  return value;
};

export const marshalUuid = (value: string) => {
  return value;
};

export enum Stage {
  Setup,
  Ready,
  Fetching,
  Errored,
  Ok,
}

export interface DateTime {}
export interface Duration {}

interface DefaultErrorHandlers {
  [index: string]: () => void;
}

const defaultErrorHandlers: DefaultErrorHandlers = {
  400: () => console.error("400"),
  404: () => console.error("404"),
  500: () => console.error("500"),
};
const defaultErrorHandler = () => {
  console.log("unknown error");
};

export type UUID = string; // base 32 string number

type MarshalMapper<IN, OUT> = (arg: IN) => OUT;

interface ParameterMarshalers {
  "date-time": MarshalMapper<Date, string>;
  number: MarshalMapper<number, string>;
  uuid: MarshalMapper<UUID, string>;
  string: MarshalMapper<string, string>;
}

export const parameterMarshalers: ParameterMarshalers = {
  "date-time": (date: Date) => date.toISOString(),
  number: (value: number) => Number(value).toString(),
  uuid: (uuid: UUID) => uuid,
  string: (value: string) => value,
};

interface BodyMarshalers {
  "date-time": MarshalMapper<Date, string>;
  number: MarshalMapper<number, number>;
  uuid: MarshalMapper<UUID, string>;
  string: MarshalMapper<string, string>;
}

export const bodyMarshalers: BodyMarshalers = {
  "date-time": (date: Date) => date.toISOString(),
  number: (value: number) => value,
  uuid: (uuid: UUID) => uuid,
  string: (value: string) => value,
};

interface Unmarshalers {
  "date-time": MarshalMapper<string, Date>;
  number: MarshalMapper<number, number>;
  uuid: MarshalMapper<string, UUID>;
  string: MarshalMapper<string, string>;
}

export const unmarshalers: Unmarshalers = {
  "date-time": (value: string) => new Date(value),
  number: (value: number) => value,
  uuid: (uuid: string) => uuid,
  string: (value: string) => value,
};

interface Parameter {
  name: string;
  value: string;
}

export type Parameters = Array<Parameter>;

export interface Result<RESPONSE_TYPE> {
  status?: number;
  stage: Stage;
  data?: RESPONSE_TYPE;
}

export interface GetArgumentsBase {}

export interface PostArgumentsBase<POST_BODY> {
  body: POST_BODY;
}

async function handleResponse<RESPONSE_TYPE>(
  response: Response,
): Promise<Result<RESPONSE_TYPE>> {
  if (!response.ok) {
    const status: string = response.status.toString();
    if (defaultErrorHandlers[status]) {
      defaultErrorHandlers[status]();
    } else {
      defaultErrorHandler();
    }
    return {
      status: response.status,
      stage: Stage.Errored,
    };
  }
  const data = await response.json();
  return {
    status: response.status,
    stage: Stage.Ok,
    data,
  };
}

const appendParameterString = (url: string, parameters: Parameters) => {
  const parameterString = parameters
    .map(({ name, value }) =>
      Array.isArray(value)
        ? value
            .map((inner) => `${name}[]=${encodeURIComponent(inner)}`)
            .join("&")
        : `${name}=${encodeURIComponent(value)}`,
    )
    .join("&");
  return parameterString ? `${url}?${parameterString}` : url;
};

export function useGet<
  WIRED_RESPONSE_TYPE,
  RESPONSE_TYPE,
  EXTERNAL_MAPPERS extends {
    [status: string]: (wired: WIRED_RESPONSE_TYPE) => RESPONSE_TYPE;
  },
>(url: string, parameters: Parameters, unmarshaler: EXTERNAL_MAPPERS) {
  const [result, setResult] = useState<Result<RESPONSE_TYPE>>({
    stage: Stage.Fetching,
  });
  useEffect(() => {
    (async () => {
      if ([Stage.Errored, Stage.Ok].includes(result.stage)) {
        return;
      }
      const wiredResponse = await handleResponse<WIRED_RESPONSE_TYPE>(
        await fetch(appendParameterString(url, parameters)),
      );
      const status = wiredResponse.status;
      if (status !== 200) {
        return {
          status,
          stage: Stage.Errored,
        };
      }
      const response = {
        ...wiredResponse,
        data: wiredResponse?.data
          ? unmarshaler[status](wiredResponse.data)
          : undefined,
      };
      setResult(response);
    })();
  });
  return result;
}

export async function doPost<
  REQUEST_TYPE,
  WIRED_RESPONSE_TYPE,
  RESPONSE_TYPE,
  EXTERNAL_MAPPERS extends {
    [status: string]: (arg: WIRED_RESPONSE_TYPE) => RESPONSE_TYPE;
  },
  EXTERNAL_HANDLERS extends { [status: string]: (arg: RESPONSE_TYPE) => void },
>(
  url: string,
  body: REQUEST_TYPE,
  externalMappers: EXTERNAL_MAPPERS,
  externalHandlers: EXTERNAL_HANDLERS,
) {
  const response = await fetch(url, {
    method: "post",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });
  const status = response.status.toString();
  if (
    !Object.keys(externalHandlers).includes(status) ||
    !Object.keys(externalMappers).includes(status)
  ) {
    throw new Error("handlable error code");
  }
  externalHandlers[status](externalMappers[status](await response.json()));
}
