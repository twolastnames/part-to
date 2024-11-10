import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../providers/ShellProvider";
import { StageMeal } from "../StageMeal";
import task1 from "../../../mocks/task1.json";
import partTo1 from "../../../mocks/partTo1.json";

test("snapshot", () => {
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
    return Promise.reject("");
  });
  render(
    <ShellProvider>
      <StageMeal />
    </ShellProvider>,
  );
  const page = screen.getByTestId("Layout");
  expect(page).toMatchSnapshot();
});
