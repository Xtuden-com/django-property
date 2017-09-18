const gulp = require('gulp'),
  sass = require('gulp-sass'),
  concat = require('gulp-concat'),
  uglify = require('gulp-uglify'),
  pixrem = require('gulp-pixrem'),
  imagemin = require('gulp-imagemin'),
  rename = require('gulp-rename'),
  cssnano = require('gulp-cssnano'),
  plumber = require('gulp-plumber'),
  path = require('path'),
  webpack = require('webpack'),
  webpackStream = require('webpack-stream'),
  UglifyJSPlugin = require('uglifyjs-webpack-plugin');

const webpackConfig = {
  context: path.resolve(__dirname, './js'),
  entry: {
    home: './home.js',
    salesearch: './salesearch.js',
    details: './details.js',
    form: './components/form.js',
  },
  output: {
    path: path.resolve(__dirname, '../static/build/js'),
    filename: '[name].bundle.js',
    libraryTarget:'window',
    library: '[name]',
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: [/node_modules/],
        use: [{
          loader: 'babel-loader',
          options: {presets: ['es2015']},
        }],
      },
      {
        test: /\.js$/,
        enforce: 'pre',
        loader: 'eslint-loader',
        options: {
          emitWarning: true,
        },
      },
    ],
  },
  plugins: [
    new webpack.optimize.CommonsChunkPlugin({
      name: 'commons',
      filename: 'commons.js',
      minChunks: 2,
    }),
    //new UglifyJSPlugin({
    //  sourceMap:true
    //})
  ],
};

gulp.task('static:img', function () {
  return gulp.src('./img/**')
    .pipe(gulp.dest('../static/build/img'));
});

gulp.task('styles', function () {
  return gulp.src('./sass/**/*.scss')
    .pipe(sass({outputStyle: 'compressed'}).on('error', sass.logError))
    .pipe(plumber())
    .pipe(cssnano())
    .pipe(pixrem())
    .pipe(rename({suffix: '.min'}))
    .pipe(gulp.dest('../static/build/css'));
});

gulp.task('scripts:app', function () {
  return gulp.src('./js/app.js')
    .pipe(plumber())
    .pipe(webpackStream(webpackConfig, webpack))
    .pipe(gulp.dest('../static/build/js'));
});

gulp.task('scripts:extra', function () {
  return gulp.src([
    './node_modules/jquery/dist/jquery.js',
    './node_modules/tether/dist/js/tether.js',
    './node_modules/popper.js/dist/umd/popper.js',
    './node_modules/bootstrap/dist/js/bootstrap.js',
  ])
    .pipe(plumber())
    .pipe(concat('extra.js'))
  //.pipe(uglify())
    .pipe(rename({suffix: '.min'}))
    .pipe(gulp.dest('../static/build/js'));
});
