var express = require('express');
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var flash = require('connect-flash');
var config = require('./config');

var app = express();

// --- Flash
app.use(flash());

// --- Static files
app.use(express.static(path.join(__dirname, 'public')));
// uncomment after placing your favicon in /public
//app.use(favicon(path.join(__dirname, 'public', 'favicon.ico')));

// --- Add user to locals
app.use(function(req, res, next) {
    res.locals.user = req.user;
    next();
});

// --- view engine setup
var exphbs = require('express-handlebars');
var hbsHelper = require('./lib/hbsHelpers');
var hbs = exphbs.create({
    helpers: hbsHelper,
    extname: '.hbs',
    defaultLayout: 'default',
    partialsDir: "views/partials/"
});
app.set('views', path.join(__dirname, 'views'));
app.engine('.hbs', hbs.engine);
app.set('view engine', '.hbs');

// --- Logger
app.use(logger('dev'));

// --- Body Parser
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
    extended: false
}));
app.use(cookieParser());

// --- Routes
var routes = require('./routes/index');
app.use('/', routes);

// --- Add the context variables
for (var key in config.context) {
    app.locals[key] = config.context[key];
}

// catch 404 and forward to error handler
app.use(function(req, res, next) {
    var err = new Error('Not Found');
    err.status = 404;

    // respond with html page
    if (req.accepts('html')) {
        res.render('404', {
            url: req.url
        });
        return;
    }

    // respond with json
    if (req.accepts('json')) {
        res.send({
            error: 'Not found'
        });
        return;
    }

    // default to plain-text. send()
    res.type('txt').send('Not found');
});

// error handlers

// development error handler
// will print stacktrace
if (app.get('env') === 'development') {
    app.use(function(err, req, res, next) {
        res.status(err.status || 500);
        res.render('error', {
            message: err.message,
            error: err
        });
    });
}

// production error handler
// no stacktraces leaked to user
app.use(function(err, req, res, next) {
    res.status(err.status || 500);
    res.render('error', {
        message: err.message,
        error: {}
    });
});


module.exports = app;
