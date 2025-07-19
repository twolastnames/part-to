import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen, waitFor } from "@testing-library/react";
import { ShellProvider } from "../../../providers/ShellProvider";
import { SelectPartTos } from "../SelectPartTos";

test("snapshot", async () => {
  fetchMock.mockResponse((request: Request) => {
    if (request.url.includes("/api/parttos/")) {
      return Promise.resolve(
        JSON.stringify({
          partTos: ["partTo1"],
        }),
      );
    }
    return Promise.reject("");
  });
  render(
    <ShellProvider>
      <SelectPartTos />
    </ShellProvider>,
  );
  await waitFor(() => {
    expect(screen.getByTestId("DynamicItemSet")).toBeTruthy();
  });
  const component = screen.getByTestId("DynamicItemSet");
  expect(component).toMatchSnapshot();
});
