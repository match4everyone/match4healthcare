const fs = require('fs')
const path = require('path')
const BundleTracker = require('webpack-bundle-tracker')
const { CleanWebpackPlugin } = require('clean-webpack-plugin')
const TerserPlugin = require('terser-webpack-plugin')

// Generate entry points from all .js files in src root
const srcDir = path.resolve(__dirname, 'src')
const entryPoints = fs
    .readdirSync(srcDir)
    .filter((fileName) => /\.js$/.test(fileName))
    .reduce((returnObject,fileName) => {
        let bundleName = fileName.split('.').slice(0,-1)
        returnObject[bundleName] = path.resolve(srcDir, fileName)
        return returnObject
    },{})

module.exports = {
    watchOptions: {
        ignored: /node_modules/,
    },
    externals: {
        jquery: 'jQuery',
    },
    context: __dirname,
    mode: 'production',
    module: {
        rules: [
            {
                test: /\.css$/,
                use: [
                    'style-loader',
                    'css-loader'
                ]
            },
            {
                test: /\.(png|jpg|gif)$/i,
                use: [
                    {
                        loader: 'url-loader',
                        options: {
                            limit: 8192,
                        },
                    },
                ],
            },
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
                        plugins: ['@babel/plugin-proposal-class-properties'],
                        presets: [
                            ['@babel/preset-env', {
                                debug: false,
                                useBuiltIns: 'usage',
                                corejs: 3,
                                targets: {
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
    entry: entryPoints, // generated from src/*.js
    output: {
        filename: '[name]-[hash].js',
        path: path.resolve(__dirname, 'dist'),
        publicPath: '/static/'
    },
    optimization: {
        minimize: true,
        minimizer: [new TerserPlugin({
            terserOptions: {
                keep_fnames: false
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