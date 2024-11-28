import React, { useEffect } from "react";
import { BrowserRouter, Route, Routes, useNavigate } from "react-router-dom";
import { getRoute } from "./routes";
import { StartMeal } from "./pages/StartMeal/StartMeal";
import { StageMeal } from "./pages/StageMeal/StageMeal";
import { Noted } from "./components/Layout/NavigationBar/Noted/Noted";
import { FourOhFour } from "./pages/FourOhFour/FourOhFour";
import { CookMeal } from "./pages/CookMeal/CookMeal";

const BaseRedirect = () => {
  const navigate = useNavigate();
  useEffect(() => {
    navigate(getRoute("StartMeal"));
  });
  return <>Redirecting ...</>;
};

export function ApplicationRouter() {
  return (
    <BrowserRouter>
      <Noted />
      <Routes>
        <Route path={getRoute("StageMeal")} element={<StageMeal />} />
        <Route path={getRoute("StartMeal")} element={<StartMeal />} />
        <Route path={getRoute("CookMeal")} element={<CookMeal />} />
        <Route path="/" element={<BaseRedirect />} />
        <Route path="*" element={<FourOhFour />} />
      </Routes>
    </BrowserRouter>
  );
}
