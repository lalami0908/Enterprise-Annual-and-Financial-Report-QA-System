const webpack = require('webpack');

module.exports = {
  transpileDependencies: [
    "vuetify"
  ],
  pages: {
    index: {
        entry: 'src/main.js',
        title: 'Chat Together'
    }
  },
  css: { extract: true },
  configureWebpack: {
    plugins: [
      new webpack.ProvidePlugin({
        $: 'jquery',
        jQuery: 'jquery',
        'windows.jQuery': 'jquery',
      }),
    ],
  },
}