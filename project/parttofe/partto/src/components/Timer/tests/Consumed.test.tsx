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
      <Timer
        consumed={getDuration(1000)}
        duration={getDuration(5000)}
        ringClasses={RingedRing}
      />
    </ShellProvider>,
  );
  const component = screen.getByTestId("Ring");
  expect(component).toMatchSnapshot();
});
