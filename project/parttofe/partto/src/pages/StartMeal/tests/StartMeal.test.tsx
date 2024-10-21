import React from "react";
import { expect, test } from "@jest/globals";
import { getAllByTestId, render, screen, waitFor, within } from "@testing-library/react";
import { StartMeal } from "../StartMeal";
import { ShellProvider } from "../../../providers/ShellProvider";
import fetchMock from "jest-fetch-mock";
import task1 from "../../../mocks/task1.json";
import partTo1 from "../../../mocks/partTo1.json";

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
    return Promise.reject("");
  });
  render(
    <ShellProvider>
      <StartMeal />
    </ShellProvider>,
  );
  const {findAllByTestId} = within(await waitFor(async () => (await screen.getAllByTestId('PartTo'))[0]))
  await findAllByTestId("Definition")
  const page = screen.getByTestId("Layout");
  expect(page).toMatchSnapshot();
});
