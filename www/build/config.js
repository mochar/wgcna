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
  }
}
