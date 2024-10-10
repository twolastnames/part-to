import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../../../providers/ShellProvider";
import { ThemeSwitch } from "../ThemeSwitch";

test("snapshot", () => {
  render(
    <ShellProvider>
      <ThemeSwitch />
    </ShellProvider>,
  );
  const component = screen.getByTestId("ThemeSwitch");
  expect(component).toBeTruthy();
});
