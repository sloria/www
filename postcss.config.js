const cssnano = require('cssnano');

const PROD = process.env.NODE_ENV === 'production';

module.exports = {
  plugins: [
    require('postcss-cssnext'),
    require('postcss-media-fn'),
    PROD && cssnano({autoprefixer: false}),
  ],
};
