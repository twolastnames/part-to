import { useEffect, useState } from "react";

const getDimensions = () => ({
  width: window.innerWidth,
  height: window.innerHeight,
});

export function useWindowResize() {
  const [{ height, width }, setDimensions] = useState<{
    height: number;
    width: number;
  }>(getDimensions());
  useEffect(() => {
    const listener = () => {
      setDimensions(getDimensions());
    };
    window.addEventListener("resize", listener);
    return () => {
      window.removeEventListener("resize", listener);
    };
  }, []);
  return { height, width };
}
