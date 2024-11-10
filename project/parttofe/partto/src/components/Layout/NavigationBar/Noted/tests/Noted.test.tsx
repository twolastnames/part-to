import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../../../providers/ShellProvider";
import { Noted } from "../Noted";

test("snapshot", () => {
  render(
    <ShellProvider>
      <Noted />
    </ShellProvider>,
  );
  const component = screen.getByTestId("NavigationBar");
  expect(component).toMatchSnapshot();
});
