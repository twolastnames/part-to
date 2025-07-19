import React from "react";
import { expect, it, describe } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../providers/ShellProvider";
import { Timer } from "../Timer";
import { getDuration } from "../../../shared/duration";
import { RingedRing } from "../Ring/Ring";

describe("color change", () => {
  beforeAll(() => {
    jest.useFakeTimers();
  });
  afterAll(() => {
    jest.useRealTimers();
  });
  it("will change", () => {
    render(
      <ShellProvider>
        <Timer duration={getDuration(5000)} ringClasses={RingedRing} />
      </ShellProvider>,
    );
    jest.advanceTimersByTime(7000);
    const component = screen.getByTestId("Ring");
    expect(component).toMatchSnapshot();
  });
});
