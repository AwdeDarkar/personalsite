import * as _ from "lodash";

function component()
{
    var element = document.createElement("div");
    element.innerHTML = _.join(["Hello", "typescript!"], " ");

    return element;
}

document.body.appendChild(component());
