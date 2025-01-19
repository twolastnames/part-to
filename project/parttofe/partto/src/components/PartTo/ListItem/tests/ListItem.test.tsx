import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen, waitFor } from "@testing-library/react";
import { ShellProvider } from "../../../../providers/ShellProvider";
import { ListItem } from "../ListItem";
import partTo1 from "../../../../mocks/partTo1.json";

test("snapshot", async () => {
  fetchMock.mockResponse((request: Request) => {
    if (request.url.includes("/api/partto/")) {
      return Promise.resolve(JSON.stringify(partTo1));
    }
    return Promise.reject("");
  });
  render(
    <ShellProvider>
      <ListItem partTo="partTo1" />
    </ShellProvider>,
  );
  await waitFor(() => {
  screen.getByTestId("ListItem");
  })
  const component = screen.getByTestId("ListItem");
  expect(component).toMatchSnapshot();
});
