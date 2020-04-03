const path = require("path");

module.exports = {
    entry: "./website/src/test.tsx",
    devtool: "inline-source-map",
    module: {
        rules: [
            {
                test: /\.ts(x?)$/,
                use: [
                    { loader: "ts-loader" }
                ],
                exclude: /node_modules/,
            },
            {
                enforce: "pre",
                test: /\.js$/,
                loader: "source-map-loader",
            }
        ],
    },
    resolve: {
        extensions: [".tsx", ".ts", ".js"],
    },
    output: {
        filename: "bundle.js",
        path: path.resolve(__dirname, "website/static")
    },
    externals: {
        "react": "React",
        "react-dom": "ReactDOM"
    }
};
