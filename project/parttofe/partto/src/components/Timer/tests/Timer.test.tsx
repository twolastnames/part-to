import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../providers/ShellProvider";
import { Timer } from "../Timer";
import { getDuration } from "../../../shared/duration";
import { RingedRing } from "../Ring/Ring";

test("snapshot", () => {
  jest.useFakeTimers();
  render(
    <ShellProvider>
      <Timer ringClasses={RingedRing} duration={getDuration(5000)} />
    </ShellProvider>,
  );
  const component = screen.getByTestId("Ring");
  expect(component).toMatchSnapshot();
});
