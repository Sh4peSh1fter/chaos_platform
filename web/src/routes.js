import Dashboard from "views/Dashboard.jsx";
import Servers from "views/Servers";
import Groups from "views/Groups";
import AddScript from "views/AddScript";


const dashboardRoutes = [
  {
    path: "/dashboard",
    name: "Dashboard",
    icon: "pe-7s-graph",
    component: Dashboard,
    layout: "/admin"
  },
  {
    path: "/groups",
    name: "Groups",
    icon: "pe-7s-note2",
    component: Groups,
    layout: "/admin",
  },
  {
    path: "/servers",
    name: "Servers",
    icon: "pe-7s-display1",
    component: Servers,
    layout: "/admin"
  }, {
    path: "/add_script",
    name: "Add Script",
    icon: "pe-7s-next-2",
    component: AddScript,
    layout: "/admin"
  }
];

export default dashboardRoutes;
