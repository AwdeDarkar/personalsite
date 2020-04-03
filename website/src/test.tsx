import * as React from "react";
import * as ReactDOM from "react-dom";

import { Hello } from "./components/Hello";

const element:React.ReactElement = <Hello compiler="TypeScript" framework="React" />;

ReactDOM.render(
    element,
    document.getElementById("example")
);
alert("Loaded");
