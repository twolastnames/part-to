import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen, waitFor } from "@testing-library/react";
import { ShellProvider } from "../../../providers/ShellProvider";
import { StageMeal } from "../StageMeal";
import task1 from "../../../mocks/task1.json";
import partTo1 from "../../../mocks/partTo1.json";
import runState1 from "../../../mocks/runState3complete.json";

const mockedUsedNavigate = jest.fn();
jest.mock("react-router-dom", () => ({
  ...(jest.requireActual("react-router-dom") as any),
  useNavigate: () => mockedUsedNavigate,
  useParams: () => ({ runState: "ourRunState" }),
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
    if (request.url.includes("/api/run/")) {
      return Promise.resolve(JSON.stringify(runState1));
    }
    if (request.url.includes("/api/task/")) {
      return Promise.resolve(JSON.stringify(task1));
    }
    if (request.method === "POST") {
      return Promise.resolve({ body: "{}", status: 404 });
    }
    return Promise.reject("");
  });
  render(
    <ShellProvider>
      <StageMeal />
    </ShellProvider>,
  );
  const adder = await waitFor(() => screen.findByLabelText("Add to Meal"));
  adder.click();
  expect(fetchMock.mock.calls.at(-1)).toBeTruthy();
  expect(
    (fetchMock.mock.calls.at(-1) || ["notpost", { method: "notpost" }])[1]
      ?.method,
  ).toEqual("post");
  expect(fetchMock.mock.calls.at(-1)?.[1]?.body || "").toEqual(
    '{"runState":"ourRunState","partTos":["partTo1"]}',
  );
  await waitFor(() => expect(mockedUsedNavigate.mock.calls).toEqual([]));
  expect(screen.getByTestId("Layout")).toMatchSnapshot();
});
