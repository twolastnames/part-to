import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../providers/ShellProvider";
import { Body } from "../Body";

test("snapshot", () => {
  render(
    <ShellProvider>
      <Body />
    </ShellProvider>,
  );
  const component = screen.getByTestId("Body");
  expect(component).toMatchSnapshot();
});
