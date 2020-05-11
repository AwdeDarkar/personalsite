import * as React from "react";
import * as ReactDOM from "react-dom";

import { Hello } from "./components/Hello";
import { RenderedEditor } from "./components/PostComponents";

import "../../node_modules/foundation-sites/scss/foundation";
import "./scss/styles.scss";

//const element:React.ReactElement = <Hello compiler="TypeScript" framework="React" />;
const editorElement:Element = document.getElementsByClassName(
    "custom-postcomponent-renderededitor")[0]
const renderedEditor:React.ReactElement = <RenderedEditor
                                           id={
                Number(editorElement.getAttribute("data-id"))} />;

ReactDOM.render(
    renderedEditor,
    editorElement
);
