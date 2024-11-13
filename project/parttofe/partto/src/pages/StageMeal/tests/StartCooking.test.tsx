import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen, waitFor } from "@testing-library/react";
import { ShellProvider } from "../../../providers/ShellProvider";
import { StageMeal } from "../StageMeal";
import task1 from "../../../mocks/task1.json";
import partTo1 from "../../../mocks/partTo1.json";
import runState1 from "../../../mocks/runState1.json";

const mockedUsedNavigate = jest.fn();
jest.mock("react-router-dom", () => ({
  ...(jest.requireActual("react-router-dom") as any),
  useNavigate: () => mockedUsedNavigate,
  useParams: () => ({ runState: "someState" }),
}));

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
      <StageMeal />
    </ShellProvider>,
  );
  const component = screen.getByTestId("Layout");
  expect(component).toMatchSnapshot();
  const start = await waitFor(() => screen.findByLabelText("Start Cooking"));
  start.click();
  expect(fetchMock.mock.calls.at(-1)).toBeTruthy();
  expect(fetchMock.mock.calls.at(-1)?.[1]?.body || "").toEqual(
    '{"runState":"someState"}',
  );
  await waitFor(() =>
    expect(mockedUsedNavigate.mock.calls).toEqual([
      ["/cook/wfGhVbmK0kzGYWqRZM2Xl3"],
    ]),
  );
});
