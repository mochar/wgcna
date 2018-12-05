'use strict'
process.env.NODE_ENV = 'production'

const exec = require('child_process').execSync
const webpack = require('webpack')
const MiniCssExtractPlugin = require("mini-css-extract-plugin")
const ProgressPlugin = require('webpack/lib/ProgressPlugin')
const OfflinePlugin = require('offline-plugin')
const base = require('./webpack.base')
const pkg = require('../package')
const _ = require('./utils')
const config = require('./config')
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin

base.mode = 'production'

exec('rm -rf dist/')
// use source-map in web app mode
base.devtool = 'cheap-module-source-map'

// use hash filename to support long-term caching
base.output.filename = '[name].[chunkhash:8].js'
// add webpack plugins
base.plugins.push(
  new ProgressPlugin(),
  new MiniCssExtractPlugin({
    filename: '[name].css',
    chunkFilename: '[id].css'
  }),
  new webpack.DefinePlugin({
    // 'ROOTURL': JSON.stringify('')
    'ROOTURL': JSON.stringify('http://localhost:5000')
  }),
  new webpack.optimize.UglifyJsPlugin({
    sourceMap: true,
    compress: {
      warnings: false
    },
    output: {
      comments: false
    }
  }),
  // progressive web app
  // it uses the publicPath in webpack config
  new OfflinePlugin({
    relativePaths: false,
    AppCache: false,
    ServiceWorker: {
      events: true
    }
  }),
  new BundleAnalyzerPlugin({
    analyzerMode: 'disable',
    generateStatsFile: true,
    statsOptions: { source: false }
  })
)

// extract css in standalone css files
_.cssProcessors.forEach(processor => {
  base.module.rules.push({
    test: processor.test,
    use: [MiniCssExtractPlugin.loader].concat(processor.use)
  })
})

// minimize webpack output
base.stats = {
  // Add children information
  children: false,
  // Add chunk information (setting this to `false` allows for a less verbose output)
  chunks: false,
  // Add built modules information to chunk information
  chunkModules: false,
  chunkOrigins: false,
  modules: false
}

module.exports = base