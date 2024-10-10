import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../../../providers/ShellProvider";
import { Detail } from "../Detail";

test("snapshot", () => {
  render(
    <ShellProvider>
      <Detail
        items={[
          {
            listView: <div>hello</div>,
            detailView: <div>hello</div>,
            itemOperations: [],
          },
          {
            listView: <div>hello</div>,
            detailView: <div>hello</div>,
            itemOperations: [],
          },
        ]}
      />
    </ShellProvider>,
  );
  const component = screen.getByTestId("Detail");
  expect(component).toMatchSnapshot();
});
