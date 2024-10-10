import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../../../providers/ShellProvider";
import { Count } from "../Count";

test("snapshot", () => {
  render(
    <ShellProvider>
      <Count on={2} total={3} />
    </ShellProvider>,
  );
  const component = screen.getByTestId("Count");
  expect(component).toMatchSnapshot();
});
