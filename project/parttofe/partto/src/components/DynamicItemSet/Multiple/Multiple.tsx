import React, { ReactElement, useState } from "react";

import classes from "./Multiple.module.scss";
import { File, List as ListIcon } from "../../Icon/Icon";
import { Button } from "../../Button/Button";
import { List } from "./List/List";
import { Detail } from "./Detail/Detail";
import { MultipleProps } from "./MultipleTypes";
import { ButtonProps } from "../../Button/ButtonTypes";
import { Item } from "../DynamicItemSetTypes";

interface View {
  toOther: ButtonProps;
  visible: (arg: Array<Item>) => ReactElement;
}

export function Multiple({ items }: MultipleProps) {
  const list: View = {
    toOther: {
      icon: File,
      text: `See all ${items.length} items in a carousel`,
      onClick: () => {
        setView(detail);
      },
    },
    visible: (items) => <List items={items} />,
  };
  const detail: View = {
    toOther: {
      icon: ListIcon,
      text: `See all ${items.length} items in a list`,
      onClick: () => {
        setView(list);
      },
    },
    visible: (items) => <Detail items={items} />,
  };
  const [{ visible, toOther }, setView] = useState<View>(detail);

  return (
    <div className={classes.multiple} data-testid="Multiple">
      <div className={classes.switchButton}>
        <Button {...toOther} />
      </div>
      {visible(items)}
    </div>
  );
}
