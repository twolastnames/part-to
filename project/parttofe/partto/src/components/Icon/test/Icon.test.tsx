import React from "react";
import { describe, expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { Icon } from "../Icon";

describe("Icon", () => {
  beforeAll(() => {
    render(<Icon />);
  });

  test("snapshot", () => {
    const component = screen.getByTestId("Icon");
    expect(component).toMatchSnapshot();
  });
});
