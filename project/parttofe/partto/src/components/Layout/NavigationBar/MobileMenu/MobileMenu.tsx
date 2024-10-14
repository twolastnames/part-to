import React, { useState } from "react";

import classes from "./MobileMenu.module.scss";
import { Burger } from "@mantine/core";
import { Menu } from "../Menu/Menu";

export function MobileMenu() {
  const [opened, setOpened] = useState<boolean>(false);
  return (
    <>
      <Burger
        classNames={classes}
        opened={opened}
        onClick={() => {
          setOpened((value) => !value);
        }}
        aria-label="Toggle Navigation"
        data-testid="MobileMenu"
        className={classes.mobileMenu}
      />
      {opened && (
        <div className={classes.menu}>
          <Menu />
        </div>
      )}
    </>
  );
}
