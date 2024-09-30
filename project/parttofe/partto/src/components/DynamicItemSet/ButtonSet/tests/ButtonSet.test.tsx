import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ButtonSet } from "../ButtonSet";
import { Start } from "../../../Icon/Icon";
import { ShellProvider } from "../../../../ShellProvider";

test("snapshot", () => {
  render(
    <ShellProvider>
      <ButtonSet
        operations={[
          {
            icon: Start,
            text: "start cooking",
            onClick: () => console.log("clicked"),
          },
        ]}
      />
    </ShellProvider>,
  );
  const component = screen.getByTestId("ButtonSet");
  expect(component).toMatchSnapshot();
});
