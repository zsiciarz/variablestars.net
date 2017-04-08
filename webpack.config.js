const path = require('path');
const webpack = require('webpack');
const ExtractTextPlugin = require("extract-text-webpack-plugin");
const WebpackShellPlugin = require("webpack-shell-plugin");

module.exports = {
    entry: {
        app: './assets/js/script.js',
        lightcurve: './assets/js/lightcurve.js',
        add_observation: './assets/js/add_observation.js',
        registration_form: './assets/js/registration_form.js',
        style: './assets/less/style.less'
    },
    output: {
        path: path.resolve(__dirname, './assets/build'),
        filename: '[name].js'
    },
    module: {
        rules: [{
            test: /\.js$/,
            exclude: /node_modules/,
            loader: 'babel-loader',
            options: {
                presets: ['es2015']
            }
        }, {
            test: /\.elm$/,
            exclude: [/elm-stuff/, /node_modules/],
            loader: 'elm-webpack-loader',
            options: {
                'pathToMake': 'node_modules/.bin/elm-make'
            },
        }, {
            test: /\.less$/,
            loader: ExtractTextPlugin.extract({
                fallback: 'style-loader',
                use: 'css-loader!less-loader'
            })
        },
        {
            test: /\.(png|woff|woff2|eot|ttf|svg)$/,
            loader: 'url-loader',
            options: {
                'limit': 100000
            }
        }, {
            test: require.resolve('jquery'),
            use: [
                {
                    loader: 'expose-loader',
                    query: 'jQuery'
                },
                {
                    loader: 'expose-loader',
                    query: '$'
                }
            ]
        }],
        noParse: [/\.elm$/]
    },
    plugins: [
        new webpack.ProvidePlugin({
            $: "jquery",
            jQuery: "jquery"
        }),
        new ExtractTextPlugin("style.css"),
        new WebpackShellPlugin({
            onBuildEnd: ["sed -i s/variablestars.net/variablestars_net/g assets/build/app.js"]
        })
    ]
};
