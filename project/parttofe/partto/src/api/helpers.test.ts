import { marshalUuid, unmarshalUuid } from "./helpers";

test("can shorten and relengthen a uuid", () => {
  expect(marshalUuid("hello")).toEqual(unmarshalUuid("hello"));
});
