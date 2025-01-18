import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../providers/ShellProvider";
import { ListItem } from "../ListItem";

test("snapshot", () => {
  render(
    <ShellProvider>
      <ListItem description="list here" />
    </ShellProvider>,
  );
  const component = screen.getByTestId("ListItem");
  expect(component).toMatchSnapshot();
});
