const path = require('path')
const BundleTracker = require('webpack-bundle-tracker')
const { CleanWebpackPlugin } = require('clean-webpack-plugin')
const TerserPlugin = require('terser-webpack-plugin')
const bundleTargetDirectory = path.resolve(__dirname, '../backend/static/bundles')

module.exports = {
  watchOptions: {
    ignored: /node_modules/,
  },
  externals: {
    jquery: 'jQuery',
    django: 'django',
  },
  context: __dirname,
  mode: 'production',
  module: {
    rules: [
      {
        test: /\.,?js$/,
        enforce: 'pre',
        loader: 'eslint-loader',
        exclude: /node_modules/,
        options: {
          emitWarning: true,
          configFile: './.eslintrc.js',
        }
      },      
      {
        test: /\.m?js$/,
        exclude: /(node_modules|bower_components)/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: [
              ['@babel/preset-env', {
                debug: false,
                'targets': {
                  'browsers': [
                    '> 0.25%, not dead',
                    'ios >= 11'
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
    path: bundleTargetDirectory,
    publicPath: '/static/bundles/'
  },
  optimization: {
    minimize: true,
    minimizer: [new TerserPlugin({
      terserOptions: {
        keep_fnames: true
      }

    })],
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
}