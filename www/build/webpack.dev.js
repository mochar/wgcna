'use strict'
process.env.NODE_ENV = 'development'

const webpack = require('webpack')
const base = require('./webpack.base')
const _ = require('./utils')
const FriendlyErrors = require('@nuxtjs/friendly-errors-webpack-plugin')

base.mode = 'development'

base.devtool = 'eval-source-map'
base.plugins.push(
  new webpack.DefinePlugin({
    'process.env.NODE_ENV': JSON.stringify('development'),
    'ROOTURL': JSON.stringify('http://localhost:5000')
  }),
  new webpack.HotModuleReplacementPlugin(),
  new webpack.NoEmitOnErrorsPlugin(),
  //new FriendlyErrors()
)

// push loader for css files
_.cssProcessors.forEach(processor => {
  base.module.rules.push(
    {
      test: processor.test,
      use: ['vue-style-loader'].concat(processor.use)
    }
  )
})

module.exports = base
