import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen, waitFor } from "@testing-library/react";
import { ShellProvider } from "../../../../providers/ShellProvider";
import { ListItem } from "../ListItem";
import task1 from "../../../../mocks/task1.json";
import runState2 from "../../../../mocks/runState2.json";
import { Duty, Imminent, Task } from "../../Icon/Icon";

test("snapshot", async () => {
  fetchMock.mockResponse((request: Request) => {
    if (request.url.includes("/api/task/")) {
      return Promise.resolve(JSON.stringify(task1));
    }
    if (request.url.includes("/api/run/")) {
      return Promise.resolve(JSON.stringify(runState2));
    }
    if (request.method === "POST") {
      return Promise.resolve(JSON.stringify({ runState: "someId" }));
    }
    return Promise.reject("");
  });
  render(
    <ShellProvider>
      <ListItem
        iconClassSets={{ imminent: Imminent, task: Task, duty: Duty }}
        task="laxed1"
        runState="anid"
      />
    </ShellProvider>,
  );
  await waitFor(() => {
    screen.getByTestId("ListItem");
  });
  const component = screen.getByTestId("ListItem");
  expect(component).toMatchSnapshot();
});
