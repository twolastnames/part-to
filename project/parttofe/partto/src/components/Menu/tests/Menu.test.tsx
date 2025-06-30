import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen, waitFor } from "@testing-library/react";
import { ShellProvider } from "../../../providers/ShellProvider";
import { Menu } from "../Menu";
import partTo1 from "../../../mocks/partTo1.json";
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
    if (request.url.includes("/api/partto/")) {
      return Promise.resolve(JSON.stringify(partTo1));
    }
    if (request.url.includes("/api/run/")) {
      return Promise.resolve(JSON.stringify(runState1));
    }
    return Promise.reject("");
  });
  render(
    <ShellProvider>
      <Menu runState="someRunStateId" />
    </ShellProvider>,
  );
  await waitFor(() => screen.findByTestId("Menu"));
  const component = screen.getByTestId("Menu");
  expect(component).toMatchSnapshot();
});
