import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../../../providers/ShellProvider";
import { addAlarmNote, Noted } from "../Noted";

test("snapshot", async () => {
  jest.useFakeTimers();
  render(
    <ShellProvider>
      <Noted />
    </ShellProvider>,
  );
  addAlarmNote({
    detail: "will still be here",
    heading: "head",
    key: "mykeyid",
  });
  expect(await screen.findByText("will still be here")).toBeTruthy();
  jest.advanceTimersByTime(28000);
  jest.useRealTimers();
  expect(await screen.findByText("will still be here")).toBeTruthy();
  const component = screen.getByTestId("NavigationBar");
  expect(component).toMatchSnapshot();
});
