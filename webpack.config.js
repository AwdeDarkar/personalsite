const path = require("path");

module.exports = {
    entry: "./website/src/test.js",
    output: {
        filename: "bundle.js",
        path: path.resolve(__dirname, "website/static")
    }
};
