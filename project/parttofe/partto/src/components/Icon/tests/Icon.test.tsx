import React from "react";
import { describe, expect, test } from "@jest/globals";
import renderer from "react-test-renderer";
import { Icon, Next } from "../Icon";

describe("Icon", () => {
  test("snapshot", () => {
    expect(
      renderer.create(<Icon definition={Next} />).toJSON(),
    ).toMatchSnapshot();
  });
});
