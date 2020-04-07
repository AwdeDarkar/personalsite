import * as React from "react";
import * as ReactDOM from "react-dom";

import { Hello } from "./components/Hello";

import "./scss/styles.scss";

const element:React.ReactElement = <Hello compiler="TypeScript" framework="React" />;

ReactDOM.render(
    element,
    document.getElementById("example")
);
