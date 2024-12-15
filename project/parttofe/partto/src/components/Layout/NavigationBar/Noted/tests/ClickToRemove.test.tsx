import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen, waitFor } from "@testing-library/react";
import { ShellProvider } from "../../../../../providers/ShellProvider";
import { addAlarmNote, Noted } from "../Noted";

test("snapshot", async () => {
  render(
    <ShellProvider>
      <Noted />
    </ShellProvider>,
  );
  addAlarmNote({
    detail: "will not still be here",
    heading: <span data-testid="bubbleup">head</span>,
  });
  expect(await screen.findByText("will not still be here")).toBeTruthy();
  const clickable = screen.getByTestId("bubbleup");
  await clickable.click();
  // eslint-disable-next-line testing-library/prefer-find-by
  await waitFor(() => expect(screen.queryAllByTestId("Note")).toEqual([]));
  const component = screen.getByTestId("NavigationBar");
  expect(component).toMatchSnapshot();
});
