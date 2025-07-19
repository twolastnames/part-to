import { useEffect, useState } from "react";
import { addErrorNote } from "../components/Layout/NavigationBar/Noted/Noted";
import { DateTime, getDateTime } from "../shared/dateTime";
import { Duration, getDuration } from "../shared/duration";

const partToApiBase = process.env.REACT_APP_PART_TO_API_BASE || "";

export enum Stage {
  Skipped,
  Fetching,
  Errored,
  Ok,
}

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
    integer: MarshalMapper<number, string>;
    number: MarshalMapper<number, string>;
    string: MarshalMapper<string, string>;
    duration: MarshalMapper<Duration, string>;
  };
  unrequired: {
    "date-time": MarshalMapper<DateTime | undefined, string | undefined>;
    integer: MarshalMapper<number | undefined, string | undefined>;
    number: MarshalMapper<number | undefined, string | undefined>;
    string: MarshalMapper<string | undefined, string | undefined>;
    duration: MarshalMapper<Duration | undefined, string | undefined>;
  };
}

export const baseParameterMarshalers: BaseParameterMarshalers = {
  required: {
    "date-time": (date: DateTime) => date.toISOString(),
    integer: (value: number) => Number(value).toString(),
    number: (value: number) => Number(value).toString(),
    string: (value: string) => value,
    duration: (value: Duration) => (value.toMilliseconds() / 1000).toString(),
  },
  unrequired: {
    "date-time": (date: DateTime | undefined) => date?.toISOString(),
    integer: (value: number | undefined) =>
      value ? Number(value).toString() : undefined,
    number: (value: number | undefined) =>
      value ? Number(value).toString() : undefined,
    string: (value: string | undefined) => value,
    duration: (value: Duration | undefined) =>
      value === undefined ? value : (value.toMilliseconds() / 1000).toString(),
  },
};

export interface BaseBodyMarshalers {
  required: {
    "date-time": MarshalMapper<DateTime, string>;
    integer: MarshalMapper<number, number>;
    number: MarshalMapper<number, number>;
    string: MarshalMapper<string, string>;
    duration: MarshalMapper<Duration, number>;
  };
  unrequired: {
    "date-time": MarshalMapper<DateTime | undefined, string | undefined>;
    number: MarshalMapper<number | undefined, number | undefined>;
    integer: MarshalMapper<number | undefined, number | undefined>;
    string: MarshalMapper<string | undefined, string | undefined>;
    duration: MarshalMapper<Duration | undefined, number | undefined>;
  };
}

export const baseBodyMarshalers: BaseBodyMarshalers = {
  required: {
    "date-time": (date: DateTime) => new Date(date.sinceEpoch()).toISOString(),
    number: (value: number) => value,
    integer: (value: number) => value,
    string: (value: string) => value,
    duration: (value: Duration) => value.toMilliseconds() / 1000,
  },
  unrequired: {
    "date-time": (date: DateTime | undefined) =>
      date ? new Date(date.sinceEpoch()).toISOString() : undefined,
    number: (value: number | undefined) => value,
    integer: (value: number | undefined) => value,
    string: (value: string | undefined) => value,
    duration: (value: Duration | undefined) =>
      value ? value.toMilliseconds() / 1000 : undefined,
  },
};

export interface BaseUnmarshalers {
  required: {
    "date-time": MarshalMapper<string, DateTime>;
    number: MarshalMapper<number, number>;
    integer: MarshalMapper<number, number>;
    string: MarshalMapper<string, string>;
    duration: MarshalMapper<number, Duration>;
    boolean: MarshalMapper<boolean, boolean>;
  };
  unrequired: {
    "date-time": MarshalMapper<string | undefined, DateTime | undefined>;
    number: MarshalMapper<number | undefined, number | undefined>;
    integer: MarshalMapper<number | undefined, number | undefined>;
    string: MarshalMapper<string | undefined, string | undefined>;
    duration: MarshalMapper<number | undefined, Duration | undefined>;
    boolean: MarshalMapper<boolean | undefined, boolean | undefined>;
  };
}

export const baseUnmarshalers: BaseUnmarshalers = {
  unrequired: {
    "date-time": (value: string | undefined) =>
      value ? getDateTime(new Date(value)) : undefined,
    duration: (value: number | undefined) =>
      value ? getDuration(value * 1000) : undefined,
    number: (value: number | undefined) => value,
    integer: (value: number | undefined) => value,
    boolean: (value: boolean | undefined) => value,
    string: (value: string | undefined) => value,
  },
  required: {
    "date-time": (value: string) => getDateTime(new Date(value)),
    duration: (value: number) => getDuration(value * 1000),
    number: (value: number) => value,
    integer: (value: number) => value,
    boolean: (value: boolean) => value,
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

const getImmutableKey = (url: string) => `immutable-${url}`;

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
  const returnable = {
    status: response.status,
    stage: Stage.Ok,
    data,
  };
  if (response.headers.get("Cache-Control")?.includes("immutable")) {
    localStorage.setItem(
      getImmutableKey(response.url),
      JSON.stringify(returnable),
    );
  }
  return returnable;
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
  const endpointUrl = partToApiBase + appendParameterString(url, parameters);
  useEffect(() => {
    const parseResult = (
      status: number,
      wiredResponse: Result<WIRED_RESPONSE_TYPE>,
    ) => {
      const response = {
        ...wiredResponse,
        data: wiredResponse?.data
          ? unmarshaler[status](wiredResponse.data)
          : undefined,
      };
      setResult(response);
    };
    const makeCall = async () => {
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
          await fetch(endpointUrl, {
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
      parseResult(status, wiredResponse);
    };
    const stored = localStorage.getItem(getImmutableKey(endpointUrl));
    if (stored) {
      const parsed = JSON.parse(stored);
      parseResult(parsed.status, parsed);
    } else {
      makeCall();
    }
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
