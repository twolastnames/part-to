import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen, waitFor } from "@testing-library/react";
import { ShellProvider } from "../../../../../providers/ShellProvider";
import { addErrorNote, Noted } from "../Noted";

test("snapshot", async () => {
  jest.useFakeTimers();
  render(
    <ShellProvider>
      <Noted />
    </ShellProvider>,
  );
  addErrorNote({ detail: "will not still be here", heading: "head" });
  expect(await screen.findByText("will not still be here")).toBeTruthy();
  jest.advanceTimersByTime(22000);
  jest.useRealTimers();
  // eslint-disable-next-line testing-library/prefer-find-by
  await waitFor(() => expect(screen.queryAllByTestId("Note")).toEqual([]));
  const component = screen.getByTestId("NavigationBar");
  expect(component).toMatchSnapshot();
});
