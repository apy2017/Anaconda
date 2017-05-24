
var webpack = require('webpack');
var path = require('path');

var BUILD_DIR = path.resolve(__dirname, '../techbot_web/static');
var APP_DIR = path.resolve(__dirname, 'src/app');

var config = {
  entry: APP_DIR + '/index.jsx',
  output: {
    path: BUILD_DIR,
    filename: 'bundle.js'
  },
  resolve: {
    extensions: ['.js', '.jsx', '.scss'],
    modules: [
      'node_modules'
    ]
  },
  module : {
    loaders : [
      {
        test : /\.jsx?/,
        include : APP_DIR,
        loader : 'babel-loader',
		query: {
                   presets: ['es2015', 'react']
               }
      },
      { test: /\.css/, loader: "style-loader!css-loader" },
	  {test: /\.scss$/, loaders: [ 'style', 'css', 'sass' ]},
      {
        test: /\.(png|jpg|)$/,
        loader: 'url-loader?limit=200000'
      },
      {
        test: /\.(ttf|eot|woff|woff2)$/,
        loader: 'file-loader',
        options: {
          name: '../techbot_web/static/fonts/[name].[ext]',
        },
      }
    ]
  }
};

module.exports = config;
