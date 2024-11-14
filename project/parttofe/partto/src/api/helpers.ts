import { useEffect, useState } from "react";
import { addErrorNote } from "../components/Layout/NavigationBar/Noted/Noted";

const partToApiBase = process.env.PART_TO_API_BASE || "http://localhost:8000";

export enum Stage {
  Skipped,
  Fetching,
  Errored,
  Ok,
}

export interface DateTime {
  sinceEpoch: () => number;
  toISOString: () => string;
  add: (arg: Duration) => DateTime;
  subtract: (arg: DateTime) => Duration;
}

export interface Duration {
  toMilliseconds: () => number;
}

export const getDateTime: (date?: Date) => DateTime = (inDate) => {
  const date = inDate || new Date();

  return {
    sinceEpoch: () => date.getTime(),
    toISOString: () => date.toISOString(),
    add: (duration: Duration) =>
      getDateTime(new Date(date.getTime() + duration.toMilliseconds())),
    subtract: (subtrahend: DateTime) =>
      getDuration(date.getTime() - subtrahend.sinceEpoch()),
  };
};

const defaultErrorHandler = async (response: Response) => {
  const heading = `Backend Error: ${response.status}`;
  const detail = await response.text();
  addErrorNote({ heading, detail });
};

const defaultExceptionHandler = async (message: string) => {
  const heading = `Backend Connection Exception`;
  const detail = message;
  addErrorNote({ heading, detail });
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
    "date-time": (date: DateTime) => new Date(date.sinceEpoch()).toISOString(),
    number: (value: number) => value,
    string: (value: string) => value,
    duration: (value: Duration) => value.toMilliseconds(),
  },
  unrequired: {
    "date-time": (date: DateTime | undefined) =>
      date ? new Date(date.sinceEpoch()).toISOString() : undefined,
    number: (value: number | undefined) => value,
    string: (value: string | undefined) => value,
    duration: (value: Duration | undefined) =>
      value ? value.toMilliseconds() : undefined,
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
  toMilliseconds: () => value,
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

export const requestStateListeners: Set<(calling: boolean) => void> = new Set();

let requestSemephore = 0;
const moveSemephore = (increment: boolean) => {
  const startState = requestSemephore > 0;
  requestSemephore += increment ? 1 : -1;
  const currentState = requestSemephore > 0;
  if (currentState === startState) {
    return;
  }
  Array.from(requestStateListeners).forEach((listener) => {
    listener(currentState);
  });
};

async function handleResponse<RESPONSE_TYPE>(
  response: Response,
): Promise<Result<RESPONSE_TYPE>> {
  if (!response.ok) {
    defaultErrorHandler(response);
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

export interface Options {
  shouldSkip?: () => boolean;
}

export function useGet<
  WIRED_RESPONSE_TYPE,
  RESPONSE_TYPE,
  EXTERNAL_MAPPERS extends {
    [status: string]: (wired: WIRED_RESPONSE_TYPE) => RESPONSE_TYPE;
  },
>(
  url: string,
  parameters: Parameters,
  unmarshaler: EXTERNAL_MAPPERS,
  options?: Options,
) {
  const [result, setResult] = useState<Result<RESPONSE_TYPE>>({
    stage: Stage.Fetching,
  });
  useEffect(() => {
    (async () => {
      if ((options?.shouldSkip || (() => false))()) {
        setResult({
          status: 0,
          stage: Stage.Skipped,
        });
        return;
      }
      let wiredResponse;
      try {
        moveSemephore(true);
        wiredResponse = await handleResponse<WIRED_RESPONSE_TYPE>(
          await fetch(partToApiBase + appendParameterString(url, parameters), {
            headers: {
              Accept: "application/json",
            },
          }),
        );
      } catch (e) {
        defaultExceptionHandler(e?.toString() || "unknown error");
        setResult({
          status: 0,
          stage: Stage.Errored,
        });
        return;
      } finally {
        moveSemephore(false);
      }
      const status = wiredResponse.status;
      if (status !== 200) {
        setResult({
          status,
          stage: Stage.Errored,
        });
        return;
      }
      const response = {
        ...wiredResponse,
        data: wiredResponse?.data
          ? unmarshaler[status](wiredResponse.data)
          : undefined,
      };
      setResult(response);
    })();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [url, JSON.stringify(parameters)]);
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
  let response;
  try {
    moveSemephore(true);
    response = await fetch(partToApiBase + url, {
      method: "post",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });
  } catch (e) {
    defaultExceptionHandler(e?.toString() || "unknown error");
    return;
  } finally {
    moveSemephore(false);
  }
  const status = response.status.toString();
  if (status !== "200") {
    defaultErrorHandler(response);
    return;
  }
  if (
    !Object.keys(externalHandlers).includes(status) ||
    !Object.keys(externalMappers).includes(status)
  ) {
    defaultExceptionHandler(`handlable error code in post to ${url}`);
    return;
  }
  externalHandlers[status](externalMappers[status](await response.json()));
}
