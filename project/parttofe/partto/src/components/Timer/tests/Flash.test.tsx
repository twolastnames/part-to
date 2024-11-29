import React from "react";
import { expect, it, describe } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../providers/ShellProvider";
import { Timer } from "../Timer";
import { getDuration } from "../../../shared/duration";

describe("text flashing", () => {
  beforeAll(() => {
    jest.useFakeTimers();
  });
  afterAll(() => {
    jest.useRealTimers();
  });
  it("will change", () => {
    render(
      <ShellProvider>
        <Timer duration={getDuration(5000)} />
      </ShellProvider>,
    );
    jest.advanceTimersByTime(12000);
    const component = screen.getByTestId("Ring");
    expect(component).toMatchSnapshot();
  });
});