import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { IterationProgress } from "../IterationProgress";
import { ShellProvider } from "../../../../../providers/ShellProvider";
import { RightContext } from "../../../../../providers/DynamicItemSetPair";

test("snapshot", () => {
  render(
    <ShellProvider>
      <IterationProgress context={RightContext} />
    </ShellProvider>,
  );
  const component = screen.getByTestId("IterationProgress");
  expect(component).toMatchSnapshot();
});
