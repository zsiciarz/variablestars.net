module.exports = {
    entry: {
        app: './assets/js/script.coffee',
        lightcurve: './assets/js/lightcurve.coffee',
        add_observation: './assets/js/add_observation.coffee',
        registration_form: './assets/js/registration_form.coffee'
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
        }]
    }
};
