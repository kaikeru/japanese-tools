var mongoose = require('mongoose');
var config = require('../config');

// Set the database
mongoose.connect(config.mongodb.uri);

// Set the promises
mongoose.Promise = require('bluebird');

module.exports = mongoose;
