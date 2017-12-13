const cssnext = require('postcss-cssnext');
const cssnano = require('cssnano');

const PROD = process.env.NODE_ENV === 'production';

module.exports = {
  plugins: [
    cssnext(),
    PROD && cssnano({autoprefixer: false}),
  ],
};
