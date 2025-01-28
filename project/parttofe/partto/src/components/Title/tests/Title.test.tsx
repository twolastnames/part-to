import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../providers/ShellProvider";
import { Title } from "../Title";
import { ChefHat } from "../../Icon/Icon";

test("snapshot", () => {
  render(
    <ShellProvider>
      <Title icon={ChefHat}>Chef hat for no reason</Title>
    </ShellProvider>,
  );
  const component = screen.getByTestId("Title");
  expect(component).toMatchSnapshot();
});
