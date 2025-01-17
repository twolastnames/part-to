import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../providers/ShellProvider";
import { PartTo } from "../PartTo";

test("snapshot", () => {
  jest.spyOn(Math, "random").mockReturnValue(0.123456789);
  render(
    <ShellProvider>
      <PartTo name="A simple part to">
        <p>More Stuff</p>
      </PartTo>
    </ShellProvider>,
  );
  const component = screen.getByTestId("PartTo");
  expect(component).toMatchSnapshot();
});
