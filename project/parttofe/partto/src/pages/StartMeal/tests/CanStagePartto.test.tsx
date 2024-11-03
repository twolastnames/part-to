import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen, waitFor } from "@testing-library/react";
import { ShellProvider } from "../../../providers/ShellProvider";
import { StartMeal } from "../StartMeal";
import task1 from "../../../mocks/task1.json";
import partTo1 from "../../../mocks/partTo1.json";

const mockedUsedNavigate = jest.fn();
jest.mock("react-router-dom", () => ({
  ...(jest.requireActual("react-router-dom") as any),
  useNavigate: () => mockedUsedNavigate,
}));

test("can stage tasks", async () => {
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
    if (request.method === "POST") {
      return Promise.resolve(JSON.stringify({ runState: "someId" }));
    }
    return Promise.reject("");
  });
  render(
    <ShellProvider>
      <StartMeal />
    </ShellProvider>,
  );
  expect(
    await screen.findByText(
      "Select recipes from the left with the arrow button to put a meal together.",
    ),
  ).toBeTruthy();
  const adder = await waitFor(() => screen.findByLabelText("Add to Meal"));
  adder.click();
  expect(fetchMock.mock.calls.at(-1)).toBeTruthy();
  expect(
    (fetchMock.mock.calls.at(-1) || ["notpost", { method: "notpost" }])[1]
      ?.method,
  ).toEqual("post");
  await waitFor(() =>
    expect(mockedUsedNavigate.mock.calls).toEqual([["/start/someId"]]),
  );
});
