import React, { ReactElement, useState } from "react";

import classes from "./Multiple.module.scss";
import { Item } from "../DynamicItemSet";
import { File, List as ListIcon } from "../../Icon/Icon";
import { Button, ButtonProps } from "../../Button/Button";
import { List } from "./List/List";
import { Detail } from "./Detail/Detail";

export interface MultipleProps {
  items: Array<Item>;
}

interface View {
  toOther: ButtonProps;
  visible: ReactElement;
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
    visible: <List items={items} />,
  };
  const detail: View = {
    toOther: {
      icon: ListIcon,
      text: `See all ${items.length} items in a list`,
      onClick: () => {
        setView(list);
      },
    },
    visible: <Detail items={items} />,
  };
  const [{ visible, toOther }, setView] = useState<View>(detail);

  return (
    <div className={classes.multiple} data-testid="Multiple">
      <div className={classes.switchButton}>
        <Button {...toOther} />
      </div>
      {visible}
    </div>
  );
}
