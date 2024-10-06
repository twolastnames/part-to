import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../../../ShellProvider";
import { Carousel } from "../Carousel";

test("snapshot", () => {
  render(
    <ShellProvider>
      <Carousel
        pages={[
          {
            view: <div>hello</div>,
          },
          {
            view: <div>world</div>,
          },
        ]}
      />
    </ShellProvider>,
  );
  const component = screen.getByTestId("Carousel");
  expect(component).toMatchSnapshot();
});
