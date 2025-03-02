const path = require('path');

module.exports = {
	mode: 'development',
	entry: './js-src/index.js',
	output: {
	    path: path.resolve(__dirname, './static/js'),
	    filename: 'xmla.js'
	}
};
