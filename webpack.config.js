const path = require("path");

const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = {
    entry: {
        main: ["./website/src/test.tsx"]
    },
    devtool: "inline-source-map",
    module: {
        rules: [
            {
                test: /\.scss$/,
                loader: [
                    MiniCssExtractPlugin.loader,
                    {
                        loader: "css-loader",
                        options: {
                            modules: true,
                            sourceMap: true
                        }
                    },
                    {
                        loader: "sass-loader",
                        options: {
                            sourceMap: true
                        }
                    }
                ],
                exclude: /node_modules/,
            },
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
    plugins: [
        new MiniCssExtractPlugin({
            filename: "styles.css",
            chunkFilename: "site.css"
        })
    ],
    resolve: {
        extensions: [".tsx", ".ts", ".js", ".scss"],
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
