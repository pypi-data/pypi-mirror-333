const path = require("path");

module.exports = {
  entry: {
    wagtail_block_exchange: "./static/wagtail_block_exchange/js/src/index.js",
  },
  output: {
    path: path.resolve(__dirname, "static/wagtail_block_exchange/js/dist"),
    filename: "[name].js",
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
          options: {
            presets: ["@babel/preset-env"],
          },
        },
      },
      {
        test: /\.css$/,
        use: ["style-loader", "css-loader"],
      },
    ],
  },
  resolve: {
    extensions: [".js"],
  },
};
