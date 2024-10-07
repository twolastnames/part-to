import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../../../ShellProvider";
import { NavigationLogo } from "../NavigationLogo";

test("snapshot", () => {
  render(
    <ShellProvider>
      <NavigationLogo />
    </ShellProvider>,
  );
  const component = screen.getByTestId("NavigationLogo");
  expect(component).toMatchSnapshot();
});
