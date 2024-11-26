import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../../../providers/ShellProvider";
import { Carousel } from "../Carousel";
import { RightContext } from "../../../../../providers/DynamicItemSetPair";

test("snapshot", () => {
  render(
    <ShellProvider>
      <Carousel
        context={RightContext}
        items={[
          {
            key: "9",
            detailView: <div>hello</div>,
            listView: <div>world</div>,
            itemOperations: [],
          },
          {
            key: "7",
            detailView: <div>world</div>,
            listView: <div>world</div>,
            itemOperations: [],
          },
        ]}
      />
    </ShellProvider>,
  );
  const component = screen.getByTestId("Carousel");
  expect(component).toMatchSnapshot();
});
