import routeKeys from "./routeKeys.json";

interface Routes {
  [key: string]: string;
}

const routes: Routes = routeKeys as Routes;

export const getRoute = (key: string) => routes[key];
