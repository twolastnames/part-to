import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen, waitFor } from "@testing-library/react";
import { ShellProvider } from "../../../providers/ShellProvider";
import { DutyClassNames, TaskDefinition } from "../TaskDefinition";
import runState2 from "../../../mocks/runState2.json";
import task1 from "../../../mocks/task1.json";
import { LeftContext } from "../../../providers/DynamicItemSetPair";

test("snapshot", async () => {
  jest.spyOn(Math, "random").mockReturnValue(0.123456789);
  jest.useFakeTimers();
  jest.setSystemTime(new Date("2025-01-02T01:03:26.200540+00:00"));
  fetchMock.mockResponse((request: Request) => {
    if (request.url.includes("/api/run/")) {
      return Promise.resolve(JSON.stringify(runState2));
    }
    if (request.url.includes("/api/task/")) {
      return Promise.resolve(JSON.stringify(task1));
    }
    return Promise.reject("");
  });
  render(
    <ShellProvider>
      <TaskDefinition
        task="enforced1"
        runState="doesnotmatter"
        locatable={{
          onLocate: (setter) => () => {},
          context: LeftContext,
        }}
        classNames={DutyClassNames}
      />
    </ShellProvider>,
  );
  await waitFor(() => {
    expect(screen.getByTestId("TaskDefinition")).toBeTruthy();
  });
  expect(screen.getByTestId("TaskDefinition")).toMatchSnapshot();
});
