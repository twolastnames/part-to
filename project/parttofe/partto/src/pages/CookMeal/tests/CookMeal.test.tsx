import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../providers/ShellProvider";
import { CookMeal } from "../CookMeal";

test("snapshot", () => {
  render(
    <ShellProvider>
      <CookMeal />
    </ShellProvider>,
  );
  const page = screen.getByTestId("Layout");
  expect(page).toMatchSnapshot();
});
