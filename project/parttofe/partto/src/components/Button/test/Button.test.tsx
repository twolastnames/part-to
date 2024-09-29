import React from "react";
import { describe, expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { Button } from "../Button";

describe("Button", () => {
  beforeAll(() => {});

  test("snapshot", () => {
    render(<Button onClick={() => undefined}>Hello</Button>);
    const component = screen.getByTestId("Button");
    expect(component).toMatchSnapshot();
  });
});
