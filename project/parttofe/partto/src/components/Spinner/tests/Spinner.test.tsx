import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../providers/ShellProvider";
import { Spinner } from "../Spinner";
import { Stage } from "../../../api/helpers";

test("snapshot", () => {
  render(
    <ShellProvider>
      <Spinner
        responses={[
          {
            stage: Stage.Ok,
          },
        ]}
      >
        <div>Not Spinning</div>
      </Spinner>
    </ShellProvider>,
  );
  const component = screen.getByTestId("Spinner");
  expect(component).toMatchSnapshot();
});
