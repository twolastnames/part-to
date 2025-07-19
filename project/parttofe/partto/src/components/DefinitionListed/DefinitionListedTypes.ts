import { ReactNode } from "react";

export interface ForData<ID_TYPE> {
  definitionKey: "ingredients" | "tools" | "description";
  id: ID_TYPE;
}

export interface ForDatas<ID_TYPE> extends Omit<ForData<ID_TYPE>, "id"> {
  ids: Array<ID_TYPE>;
}

export interface DefinitionListedProps {
  summary: ReactNode;
  children: ReactNode;
}
