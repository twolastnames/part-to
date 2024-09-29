import { useEffect, useState } from "react";

export enum Stage {
  Setup,
  Ready,
  Fetching,
  Errored,
  Ok,
}

export interface DateTime {
  epoch: () => number;
  toISOString: () => string;
}

export const getDateTime: (date?: Date) => DateTime = (date) => ({
  epoch: () => (date || new Date()).getDate(),
  toISOString: () => (date || new Date()).toISOString(),
});

export interface Duration {
  inMilliseconds: () => number;
}

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

export type MarshalMapper<IN, OUT> = (arg: IN) => OUT;

export interface BaseParameterMarshalers {
  required: {
    "date-time": MarshalMapper<DateTime, string>;
    number: MarshalMapper<number, string>;
    string: MarshalMapper<string, string>;
  };
  unrequired: {
    "date-time": MarshalMapper<DateTime | undefined, string | undefined>;
    number: MarshalMapper<number | undefined, string | undefined>;
    string: MarshalMapper<string | undefined, string | undefined>;
  };
}

export const baseParameterMarshalers: BaseParameterMarshalers = {
  required: {
    "date-time": (date: DateTime) => date.toISOString(),
    number: (value: number) => Number(value).toString(),
    string: (value: string) => value,
  },
  unrequired: {
    "date-time": (date: DateTime | undefined) => date?.toISOString(),
    number: (value: number | undefined) =>
      value ? Number(value).toString() : undefined,
    string: (value: string | undefined) => value,
  },
};

export interface BaseBodyMarshalers {
  required: {
    "date-time": MarshalMapper<DateTime, string>;
    number: MarshalMapper<number, number>;
    string: MarshalMapper<string, string>;
    duration: MarshalMapper<Duration, number>;
  };
  unrequired: {
    "date-time": MarshalMapper<DateTime | undefined, string | undefined>;
    number: MarshalMapper<number | undefined, number | undefined>;
    string: MarshalMapper<string | undefined, string | undefined>;
    duration: MarshalMapper<Duration | undefined, number | undefined>;
  };
}

export const baseBodyMarshalers: BaseBodyMarshalers = {
  required: {
    "date-time": (date: DateTime) => new Date(date.epoch()).toISOString(),
    number: (value: number) => value,
    string: (value: string) => value,
    duration: (value: Duration) => value.inMilliseconds(),
  },
  unrequired: {
    "date-time": (date: DateTime | undefined) =>
      date ? new Date(date.epoch()).toISOString() : undefined,
    number: (value: number | undefined) => value,
    string: (value: string | undefined) => value,
    duration: (value: Duration | undefined) =>
      value ? value.inMilliseconds() : undefined,
  },
};

export interface BaseUnmarshalers {
  required: {
    "date-time": MarshalMapper<string, DateTime>;
    number: MarshalMapper<number, number>;
    string: MarshalMapper<string, string>;
    duration: MarshalMapper<number, Duration>;
  };
  unrequired: {
    "date-time": MarshalMapper<string | undefined, DateTime | undefined>;
    number: MarshalMapper<number | undefined, number | undefined>;
    string: MarshalMapper<string | undefined, string | undefined>;
    duration: MarshalMapper<number | undefined, Duration | undefined>;
  };
}

export const getDuration: (arg: number) => Duration = (value) => ({
  inMilliseconds: () => value,
});

export const baseUnmarshalers: BaseUnmarshalers = {
  unrequired: {
    "date-time": (value: string | undefined) =>
      value ? getDateTime(new Date(value)) : undefined,
    duration: (value: number | undefined) =>
      value ? getDuration(value) : undefined,
    number: (value: number | undefined) => value,
    string: (value: string | undefined) => value,
  },
  required: {
    "date-time": (value: string) => getDateTime(new Date(value)),
    duration: (value: number) => getDuration(value),
    number: (value: number) => value,
    string: (value: string) => value,
  },
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