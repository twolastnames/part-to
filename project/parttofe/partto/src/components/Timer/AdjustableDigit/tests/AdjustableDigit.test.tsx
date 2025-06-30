import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../../providers/ShellProvider";
import { AdjustableDigit } from "../AdjustableDigit";

test("snapshot", () => {
  render(
    <ShellProvider>
      <AdjustableDigit increment={() => {}} decrement={() => {}}>
        5
      </AdjustableDigit>
    </ShellProvider>,
  );
  const component = screen.getByTestId("AdjustableDigit");
  expect(component).toMatchSnapshot();
});
