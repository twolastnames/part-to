import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen, waitFor } from "@testing-library/react";
import { ShellProvider } from "../../../../../providers/ShellProvider";
import { Detail } from "../Detail";
import { getDateTime } from "../../../../../shared/dateTime";
import { getDuration } from "../../../../../shared/duration";
import task1 from "../../../../../mocks/task1.json";

test("snapshot", async () => {
  jest.useFakeTimers();
  jest.setSystemTime(new Date(Date.parse("04 Dec 2022 00:12:00 GMT")));
  fetchMock.mockResponse((request: Request) => {
    if (request.url.includes("/api/task/")) {
      return Promise.resolve(JSON.stringify(task1));
    }
    if (request.method === "POST") {
      return Promise.resolve(JSON.stringify({ runState: "someId" }));
    }
    return Promise.reject("");
  });
  render(
    <ShellProvider>
      <Detail
        timestamp={getDateTime(
          new Date(Date.parse("04 Dec 2022 00:12:00 GMT")),
        )}
        till={getDuration(3000)}
        duty="someId"
      />
    </ShellProvider>,
  );
  // eslint-disable-next-line testing-library/prefer-find-by
  const component = await waitFor(() => screen.getByTestId("Detail"));
  expect(component).toMatchSnapshot();
});
