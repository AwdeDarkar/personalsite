import _ from "lodash";

function component()
{
    var element = document.createElement("div");
    element.innerHTML = _.join(["Test","js","worked"]);

    return element;
}

document.body.appendChild(component());