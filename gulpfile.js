const gulp = require("gulp");
const css = () => {
    const postCss = require('gulp-postcss');
    // const sass = require('gulp-sass');
    const sass = require('gulp-sass')(require('sass'));
    const minify = require('gulp-csso');
    sass.compiler = require('node-sass');
    return gulp
        .src('assets/scss/styles.scss')
        .pipe(sass().on('errors', sass.logError))
        .pipe(postCss([require('tailwindcss'), require('autoprefixer')]))
        .pipe(minify())
        .pipe(gulp.dest('static/css'))
}
exports.default = css;