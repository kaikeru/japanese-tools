/* Gulp task runner for SASS processing and Javascript processing */

// IMPORTS
var gulp = require('gulp'),
    sass = require('gulp-sass'),
    cleanCSS = require('gulp-clean-css'),
    rename = require('gulp-rename'),
    browserify = require('gulp-browserify');

// GLOBALS
var jsDest = 'src/js';
var cssDest = 'public/css'
var npmJSFiles = 'node_modules'

/**
 * Process the CSS
 */
gulp.task('styles', function() {
    return gulp.src('src/sass/**/*.scss')
        .pipe(sass({
                includePaths: [
                    'node_modules/bootstrap-sass/assets/stylesheets',
            ]
            })
        .on('error', sass.logError))
        .pipe(cleanCSS({compatibility: 'ie8'}))
        .pipe(gulp.dest(cssDest))
});

/**
 * Process the JS
 */
/**
 * Bundle the JS
 */
gulp.task('browserify', function() {
    // Single entry point to browserify
    gulp.src('src/js/app.js')
        .pipe(browserify({
            insertGlobals: true,
            debug: !gulp.env.production
        }))
        .pipe(gulp.dest('public/js'))
});

/**
 * Watch task
 */
gulp.task('watch', ['styles', 'browserify'], function() {
    gulp.watch('src/sass/**/*.scss', ['styles']);
    //gulp.watch('node_modules/**/*.js', ['jsProcess']);
    gulp.watch('src/js/**/*.js', ['browserify']);
});

/**
 * Default task
 */
gulp.task('default', ['styles', 'jsMove', 'browserify']);
