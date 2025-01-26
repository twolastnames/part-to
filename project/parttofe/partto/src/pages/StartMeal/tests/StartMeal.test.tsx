import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen, waitFor, within } from "@testing-library/react";
import { StartMeal } from "../StartMeal";
import { ShellProvider } from "../../../providers/ShellProvider";
import fetchMock from "jest-fetch-mock";
import task2 from "../../../mocks/task2.json";
import partTo1 from "../../../mocks/partTo1.json";

test("snapshot", async () => {
  jest.spyOn(Math, "random").mockReturnValue(0.123456789);
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
      return Promise.resolve(JSON.stringify(task2));
    }
    return Promise.reject("");
  });
  render(
    <ShellProvider>
      <StartMeal />
    </ShellProvider>,
  );
  const { findAllByTestId } = within(
    await waitFor(async () => screen.getAllByTestId("DetailShell")[0]),
  );
  await findAllByTestId("Accordion");
  const page = screen.getByTestId("Layout");
  expect(page).toMatchSnapshot();
});
