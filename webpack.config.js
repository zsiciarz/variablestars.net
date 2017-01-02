var webpack = require('webpack');
var ExtractTextPlugin = require("extract-text-webpack-plugin");
var WebpackShellPlugin = require("webpack-shell-plugin");

module.exports = {
    entry: {
        app: './assets/js/script.coffee',
        lightcurve: './assets/js/lightcurve.coffee',
        add_observation: './assets/js/add_observation.coffee',
        registration_form: './assets/js/registration_form.coffee',
        style: './assets/less/style.less'
    },
    output: {
        path: './assets/build',
        filename: '[name].js'
    },
    module: {
        loaders: [{
            test: /\.coffee$/,
            exclude: /node_modules/,
            loader: 'coffee'
        }, {
            test: /\.elm$/,
            exclude: [/elm-stuff/, /node_modules/],
            loader: 'elm-webpack?pathToMake=node_modules/.bin/elm-make'
        }, {
            test: /\.less$/,
            loader: ExtractTextPlugin.extract("style-loader", "css-loader!less-loader")
        },
        {
            test: /\.(png|woff|woff2|eot|ttf|svg)$/,
            loader: 'url-loader?limit=100000'
        }, {
            test: require.resolve("jquery"),
            loader: "expose?$!expose?jQuery"
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
