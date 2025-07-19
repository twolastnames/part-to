import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen, waitFor } from "@testing-library/react";
import { ShellProvider } from "../../../../../providers/ShellProvider";
import duty1 from "../../../../../mocks/duty1.json";
import runState2 from "../../../../../mocks/runState2.json";
import { TaskTitle } from "../TaskTitle";

test("snapshot", async () => {
  fetchMock.mockResponse((request: Request) => {
    if (request.url.includes("/api/task/")) {
      return Promise.resolve(JSON.stringify(duty1));
    }
    if (request.url.includes("/api/run/")) {
      return Promise.resolve(JSON.stringify(runState2));
    }
    return Promise.reject("");
  });
  render(
    <ShellProvider>
      <TaskTitle task="enforced1" runState="somerunstate" />
    </ShellProvider>,
  );
  // eslint-disable-next-line testing-library/prefer-find-by
  const component = await waitFor(() => screen.getByTestId("Title"));
  expect(component).toMatchSnapshot();
});
