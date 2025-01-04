import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen, waitFor } from "@testing-library/react";
import { ShellProvider } from "../../../providers/ShellProvider";
import { ManageTasks } from "../ManageTasks";
import { LeftContext } from "../../../providers/DynamicItemSetPair";
import task1 from "../../../mocks/task1.json";
import partTo1 from "../../../mocks/partTo1.json";
import runState1 from "../../../mocks/runState1.json";
import { TaskClassNames } from "../../TaskDefinition/TaskDefinition";

test("snapshot", async () => {
  fetchMock.mockResponse((request: Request) => {
    if (request.url.includes("/api/parttos/")) {
      return Promise.resolve(
        JSON.stringify({
          partTos: ["partTo1"],
        }),
      );
    }
    if (request.url.includes("/api/partto/")) {
      return Promise.resolve(JSON.stringify(partTo1));
    }
    if (request.url.includes("/api/task/")) {
      return Promise.resolve(JSON.stringify(task1));
    }
    if (request.url.includes("/api/run/")) {
      return Promise.resolve(JSON.stringify(runState1));
    }
    if (request.method === "POST") {
      return Promise.resolve(JSON.stringify({ runState: "someId" }));
    }
    return Promise.reject("");
  });
  render(
    <ShellProvider>
      <div data-testid="ManageTasks">
        <ManageTasks
          context={LeftContext}
          emptyText="Empty Yo"
          tasks={["a", "task", "list"]}
          definitionClassNames={TaskClassNames}
        />{" "}
      </div>
    </ShellProvider>,
  );
  await waitFor(() => {
    expect(screen.getAllByTestId("DynamicItemSet")).toBeTruthy();
  });
  const component = screen.getByTestId("ManageTasks");
  expect(component).toMatchSnapshot();
});
