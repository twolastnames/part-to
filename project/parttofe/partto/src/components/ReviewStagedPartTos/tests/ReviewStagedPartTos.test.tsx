import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen, waitFor } from "@testing-library/react";
import { ShellProvider } from "../../../providers/ShellProvider";
import { ReviewStagedPartTos } from "../ReviewStagedPartTos";
import runState1 from "../../../mocks/runState1.json";

test("snapshot", async () => {
  fetchMock.mockResponse((request: Request) => {
    if (request.url.includes("/api/parttos/")) {
      return Promise.resolve(
        JSON.stringify({
          partTos: ["partTo1"],
        }),
      );
    }
    if (request.url.includes("/api/run/")) {
      return Promise.resolve(JSON.stringify(runState1));
    }
    return Promise.reject("");
  });
  render(
    <ShellProvider>
      <ReviewStagedPartTos taskDefinitions={["Hello", "World"]} />
    </ShellProvider>,
  );
  await waitFor(() => {
    expect(screen.getByTestId("DynamicItemSet")).toBeTruthy();
  });
  const component = screen.getByTestId("DynamicItemSet");
  expect(component).toMatchSnapshot();
});
