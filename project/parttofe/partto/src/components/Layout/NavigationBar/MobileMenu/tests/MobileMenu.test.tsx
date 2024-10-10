import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../../../providers/ShellProvider";
import { MobileMenu } from "../MobileMenu";

test("snapshot", () => {
  render(
    <ShellProvider>
      <MobileMenu />
    </ShellProvider>,
  );
  const component = screen.getByTestId("MobileMenu");
  expect(component).toMatchSnapshot();
});
