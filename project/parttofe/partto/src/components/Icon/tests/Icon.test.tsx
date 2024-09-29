import React from "react";
import { describe, expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { Icon, Next } from "../Icon";

describe("Icon", () => {
  test("snapshot", () => {
    render(<Icon definition={Next} />);
    const component = screen.getByTestId("Icon");
    expect(component).toMatchSnapshot();
  });
});
