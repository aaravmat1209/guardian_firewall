const webpack = require('webpack');

module.exports = {
  webpack: {
    configure: (webpackConfig) => {
      // Add fallbacks for Node.js modules
      webpackConfig.resolve.fallback = {
        ...webpackConfig.resolve.fallback,
        "crypto": require.resolve("crypto-browserify"),
        "stream": require.resolve("stream-browserify"),
        "buffer": require.resolve("buffer"),
        "process": require.resolve("process/browser"),
        "util": require.resolve("util"),
        "url": require.resolve("url"),
        "querystring": require.resolve("querystring-es3"),
        "path": require.resolve("path-browserify"),
        "fs": false,
        "net": false,
        "tls": false,
        "child_process": false,
        "os": false,
        "http": false,
        "https": false,
        "zlib": false
      };

      // Add plugins for global variables
      webpackConfig.plugins = [
        ...webpackConfig.plugins,
        new webpack.ProvidePlugin({
          Buffer: ['buffer', 'Buffer'],
          process: 'process/browser',
        }),
      ];

      // Ignore Node.js modules that can't be polyfilled
      webpackConfig.ignoreWarnings = [
        /Failed to parse source map/,
        /Module not found: Error: Can't resolve 'node:/,
      ];

      return webpackConfig;
    },
  },
};
