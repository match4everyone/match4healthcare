const path = require('path');
const BundleTracker = require('webpack-bundle-tracker')
const { CleanWebpackPlugin } = require('clean-webpack-plugin');

module.exports = {
  watchOptions: {
    ignored: /node_modules/,
  },
  context: __dirname,
  mode: 'production',
  module: {
    rules: [
      {
        test: /\.m?js$/,
        exclude: /(node_modules|bower_components)/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: [
              ["@babel/preset-env", {
                debug: false,
                "targets": {
                  "browsers": [
                    "> 0.25%, not dead",
                    "ios >= 11"
                  ]
                }
            }]
            ]
          }
        }
      }
    ]
  },
  entry: {
    main: ['./src/main.js'],
    student: ['./src/student.js'],
  },
  output: {
    filename: '[name]-[hash].js',
    path: path.resolve(__dirname, 'dist'),
    publicPath: '/static/'
  },
  plugins: [
    new CleanWebpackPlugin(),
    new BundleTracker({
      path: __dirname,
      filename: 'webpack-stats.json',
      logTime: true,
      indent: '\t',
    }),
  ],
};