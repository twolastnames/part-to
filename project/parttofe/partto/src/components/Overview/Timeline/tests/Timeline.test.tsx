import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../../providers/ShellProvider";
import { Timeline } from "../Timeline";

test("snapshot", () => {
  render(
    <ShellProvider>
      <Timeline runState="some id" />
    </ShellProvider>,
  );
  const component = screen.getByTestId("Accordion");
  expect(component).toMatchSnapshot();
});
