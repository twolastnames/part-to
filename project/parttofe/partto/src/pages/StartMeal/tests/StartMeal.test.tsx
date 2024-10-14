import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { StartMeal } from "../StartMeal";
import { ShellProvider } from "../../../providers/ShellProvider";
import fetchMock from "jest-fetch-mock";

test("snapshot", () => {
  fetchMock.mockResponse((request: Request) => {
    if (request.url.includes("/api/parttos/")) {
      return Promise.resolve(
        JSON.stringify({
          partTos: ["partTo1", "partTo2", "partTo3"],
        }),
      );
    }
    return Promise.reject("");
  });
  render(
    <ShellProvider>
      <StartMeal />
    </ShellProvider>,
  );
  const page = screen.getByTestId("Layout");
  expect(page).toMatchSnapshot();
});
