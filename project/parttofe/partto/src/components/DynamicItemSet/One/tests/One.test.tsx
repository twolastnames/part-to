import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { One } from "../One";

test("snapshot", () => {
  render(
    <One
      item={{
        listView: <div>invisible</div>,
        detailView: <div>shown</div>,
        itemOperations: [],
      }}
    />,
  );

  const component = screen.getByTestId("One");
  expect(component).toMatchSnapshot();
});
