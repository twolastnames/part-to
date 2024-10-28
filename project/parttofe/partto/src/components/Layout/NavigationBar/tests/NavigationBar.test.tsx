import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../../providers/ShellProvider";
import { NavigationBar } from "../NavigationBar";

test("snapshot", () => {
  render(
    <ShellProvider>
      <NavigationBar extra="hello world">Hello</NavigationBar>
    </ShellProvider>,
  );
  const component = screen.getByTestId("NavigationBar");
  expect(component).toBeTruthy();
});
