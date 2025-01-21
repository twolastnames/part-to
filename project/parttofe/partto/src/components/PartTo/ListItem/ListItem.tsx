import React from "react";

import { ListItemProps } from "./ListItemTypes";
import { ListItem as GenericListItem } from "../../ListItem/ListItem";
import { useParttoGet } from "../../../api/parttoget";
import { Spinner } from "../../Spinner/Spinner";
import { Recipe } from "../../Icon/Icon";

export function ListItem({ partTo }: ListItemProps) {
  const response = useParttoGet({ partTo });
  return (
    <Spinner responses={[response]}>
      <GenericListItem
        precursor={<Recipe />}
        description={response.data?.name}
      />
    </Spinner>
  );
}
