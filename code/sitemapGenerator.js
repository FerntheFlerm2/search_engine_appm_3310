const SitemapGenerator = require('sitemap-generator');

//NOTES:
// https://docs.npmjs.com/downloading-and-installing-node-js-and-npm
//h ttps://www.npmjs.com/package/sitemap-generator

//TO USE:
// run using node sitemapGenerator.js


// create generator
const generator = SitemapGenerator('https://www.colorado.edu/', {
  maxDepth: 4,
  maxEntriesPerFile: 10000,
  stripQuerystring: false
});

var i = 0;

// register event listeners
generator.on('done', () => {
  console.log("Done.");
  // say done upon completion
});

// every 50 adds, print how many resources have been added
generator.on('add', (url) => {
  i += 1;
  if (i % 50 == 0) {
    console.log("Added " + i + " resources");
  }
});

// output all errors
generator.on('error', (error) => {
  console.log(error);
});

// start the sitemap generator
generator.start();

// saves output to sitemap.xml
