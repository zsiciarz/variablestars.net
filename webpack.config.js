module.exports = {
    entry: './assets/js/script.coffee',
    output: {
        path: './assets/build',
        filename: 'app.js'
    },
    module: {
        loaders: [{
            test: /\.coffee$/,
            exclude: /node_modules/,
            loader: 'coffee'
        }]
    }
};
