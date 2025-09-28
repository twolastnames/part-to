import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen, waitFor } from "@testing-library/react";
import { ShellProvider } from "../../../providers/ShellProvider";
import { Version } from "../Version";
import versionResponse from "../../../mocks/version.json";

test("snapshot", async () => {
  fetchMock.mockResponse((request: Request) => {
    return Promise.resolve(JSON.stringify(versionResponse));
  });
  render(
    <ShellProvider>
      <Version />
    </ShellProvider>,
  );
  await waitFor(() => {
    expect(screen.getByTestId("Version")).toBeTruthy();
  });
  const component = screen.getByTestId("Version");
  expect(component).toMatchSnapshot();
});
