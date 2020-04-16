import * as React from "react";
import * as ReactDOM from "react-dom";

import { Hello } from "./components/Hello";

import "../../node_modules/foundation-sites/scss/foundation";
import "./scss/styles.scss";

const element:React.ReactElement = <Hello compiler="TypeScript" framework="React" />;

/* Example react code for adding the `element` to the page
ReactDOM.render(
    element,
    document.getElementById("example")
);
*/
