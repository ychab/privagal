var gulp = require('gulp'),
    jshint = require('gulp-jshint'),
    uglify = require('gulp-uglify'),
    minifyCss = require('gulp-minify-css'),
    less = require('gulp-less'),
    concat = require('gulp-concat'),
    sourcemaps = require('gulp-sourcemaps');

gulp.task('js', ['jshint'], function () {
  return gulp.src([
    'privagal/static/bower_components/jquery/jquery.js',
    'privagal/static/bower_components/bootstrap/dist/js/bootstrap.js',
    'privagal/static/bower_components/picturefill/dist/picturefill.js',
    'privagal/static/bower_components/imagesloaded/imagesloaded.pkgd.js',
    'privagal/static/bower_components/packery/dist/packery.pkgd.js',
    'privagal/static/bower_components/infinite-ajax-scroll/src/jquery-ias.js',
    'privagal/static/bower_components/infinite-ajax-scroll/src/callbacks.js',
    'privagal/static/bower_components/infinite-ajax-scroll/src/extension/spinner.js',
    'privagal/static/bower_components/infinite-ajax-scroll/src/extension/noneleft.js',
    'privagal/static/privagal/src/js/**/*.js'
  ])
    .pipe(sourcemaps.init())
    .pipe(concat('privagal.min.js'))
    .pipe(uglify())
    .pipe(sourcemaps.write())
    .pipe(gulp.dest('privagal/static/privagal/dist/js/'));
});

gulp.task('less', function () {
  return gulp.src([
    'privagal/static/privagal/src/less/**/*.less'
  ])
    .pipe(sourcemaps.init())
    .pipe(less({
        paths: ['privagal/static/bower_components']
    }))
    .pipe(concat('privagal.min.css'))
    .pipe(minifyCss())
    .pipe(sourcemaps.write())
    .pipe(gulp.dest('privagal/static/privagal/dist/css/'));
});

gulp.task('jshint', function() {
  return gulp.src('privagal/static/privagal/src/js/**/*.js')
    .pipe(jshint())
    .pipe(jshint.reporter('default'));
});

gulp.task('watch', function () {
  gulp.watch(['privagal/static/privagal/src/js/**/*.js'], ['js']);
  gulp.watch(['privagal/static/privagal/src/less/**/*.less'], ['less']);
});

gulp.task('default', ['js', 'less']);
