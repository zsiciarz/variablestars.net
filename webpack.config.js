var ExtractTextPlugin = require("extract-text-webpack-plugin");
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
            test: /\.less$/,
            loader: ExtractTextPlugin.extract("style-loader", "css-loader!less-loader")
        }]
    },
    plugins: [
        new ExtractTextPlugin("style.css")
    ]
};
