import routeKeys from "./routeKeys.json";

interface Routes {
  [key: string]: string;
}

const routes: Routes = routeKeys as Routes;

interface Substitutions {
  [arg: string]: string;
}

export const getRoute = (key: string, substitutions?: Substitutions) =>
  `/${Object.entries(substitutions || {}).reduce(
    (current, [key, value]) => current.replace(`:${key}`, value),
    routes[key],
  )}`;
