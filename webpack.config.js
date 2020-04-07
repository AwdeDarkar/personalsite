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
                test: /\.s(c|a)ss$/,
                use: [
                    {
                        loader: MiniCssExtractPlugin.loader,
                    },
                    {
                        loader: "css-loader",
                        options: {
                            modules: true,
                            sourceMap: true,
                            modules: {
                                localIdentName: "[local]"
                            }
                        },
                    },
                    {
                        loader: "postcss-loader",
                        options: {
                            sourceMap: true,
                            config: {
                                path: "postcss.config.js"
                            },
                        }
                    },
                    {
                        loader: "sass-loader",
                        options: {
                            sourceMap: true,
                        }
                    }
                ],
                include: [
                    path.resolve(__dirname, "node_modules/foundation-sites/scss/foundation"),
                    path.resolve(__dirname, "website/src/scss"),
                ]
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
