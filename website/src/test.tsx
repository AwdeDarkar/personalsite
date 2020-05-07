import * as React from "react";
import * as ReactDOM from "react-dom";

import { Hello } from "./components/Hello";
import { RenderedEditor } from "./components/PostComponents";

import "../../node_modules/foundation-sites/scss/foundation";
import "./scss/styles.scss";

//const element:React.ReactElement = <Hello compiler="TypeScript" framework="React" />;
const renderedEditor:React.ReactElement = <RenderedEditor />;

ReactDOM.render(
    renderedEditor,
    document.getElementsByClassName("custom-postcomponent-renderededitor")[0]
);
