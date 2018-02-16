'use strict'
const pkg = require('../package')

module.exports = {
  port: 4000,
  title: 'WGCNA',
  publicPath: '/',
  vendor: Object.keys(pkg.dependencies),
  babel: {
    babelrc: false,
    presets: ['vue-app']
  },
  postcss: [
    // add prefix via postcss since it's faster
    require('autoprefixer')({
      // Vue does not support ie 8 and below
      browsers: ['last 2 versions', 'ie > 8']
    }),
    require('postcss-nested')
  ],
  cssModules: true
}
