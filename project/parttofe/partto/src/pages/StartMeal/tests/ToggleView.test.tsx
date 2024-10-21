import React from "react";
import { expect, test } from "@jest/globals";
import { fireEvent, render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../providers/ShellProvider";
import { StartMeal } from "../StartMeal";
import task1 from "../../../mocks/task1.json";
import partTo1 from "../../../mocks/partTo1.json";

test("toggle to list", async () => {
  fetchMock.mockResponse((request: Request) => {
    if (request.url.includes("/api/parttos/")) {
      return Promise.resolve(
        JSON.stringify({
          partTos: ["partTo1", "partTo2"],
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
      <StartMeal />
    </ShellProvider>,
  );
  const toggle = await screen.findByLabelText("See all 2 items in a list");
  await fireEvent.click(toggle);
  const component = await screen.findByTestId("Layout");
  expect(component).toMatchSnapshot();
});
