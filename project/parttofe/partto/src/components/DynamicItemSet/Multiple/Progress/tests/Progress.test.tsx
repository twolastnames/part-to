import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../../../providers/ShellProvider";
import { Progress } from "../Progress";

test("snapshot", () => {
  render(
    <ShellProvider>
      <Progress on={5} total={7} label={"11"} />
    </ShellProvider>,
  );
  const component = screen.getByTestId("LocalProgress");
  expect(component).toMatchSnapshot();
});
