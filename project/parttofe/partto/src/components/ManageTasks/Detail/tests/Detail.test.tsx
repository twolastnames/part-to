import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen, waitFor } from "@testing-library/react";
import { ShellProvider } from "../../../../providers/ShellProvider";
import { Detail } from "../Detail";
import task1 from "../../../../mocks/task1.json";
import runState1 from "../../../../mocks/runState1.json";
import metricTask1 from "../../../../mocks/metricTask1.json";

test("snapshot", async () => {
  fetchMock.mockResponse((request: Request) => {
    if (request.url.includes("/api/run/")) {
      return Promise.resolve(JSON.stringify(runState1));
    }
    if (request.url.includes("/api/task/")) {
      return Promise.resolve(JSON.stringify(task1));
    }
    if (request.url.includes("/api/metric/task")) {
      return Promise.resolve(JSON.stringify(metricTask1));
    }
    return Promise.reject("");
  });
  render(
    <ShellProvider>
      <Detail task="aTask" runState="aRunState" />
    </ShellProvider>,
  );
  const component = await waitFor(() => {
    screen.getByTestId("Detail");
  });
  expect(component).toMatchSnapshot();
});
