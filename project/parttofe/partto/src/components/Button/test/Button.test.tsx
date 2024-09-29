import React from "react";
import { describe, expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { Button } from "../Button";

describe("Button", () => {
  beforeAll(() => {
    render(<Button onClick={() => undefined}>Hello</Button>);
  });

  test("snapshot", () => {
    const component = screen.getByTestId("Button");
    expect(component).toMatchSnapshot();
  });
});
