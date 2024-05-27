/*
 * Main Javascript file for inventory.
 *
 * This file bundles all of your javascript together using webpack.
 */

// JavaScript modules
require('@fortawesome/fontawesome-free');
require('jquery');
require('bootstrap');
require('chart.js');

require.context(
  '../img', // context folder
  true, // include subdirectories
  /.*/, // RegExp
);

// Your own code
require('./plugins');
require('./script');
require('./location');
require('./machine');
require('./tool');
require('./user');
require('./dashboard');
