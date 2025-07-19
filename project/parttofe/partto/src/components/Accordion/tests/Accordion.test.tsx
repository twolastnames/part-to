import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../providers/ShellProvider";
import { Accordion } from "../Accordion";

test("snapshot", () => {
  render(
    <ShellProvider>
      <Accordion summary="A Summary">
        <ul>
          <li>Some</li>
          <li>List</li>
        </ul>
      </Accordion>
    </ShellProvider>,
  );
  const component = screen.getByTestId("Accordion");
  expect(component).toMatchSnapshot();
});
