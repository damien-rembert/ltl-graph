/**
 * @type {import('gatsby').GatsbyConfig}
 */

require("dotenv").config({
  path: `.env.${process.env.NODE_ENV}`,
});

module.exports = {
  siteMetadata: {
    title: `ltl-usage-graph`,
    siteUrl: `https://www.yourdomain.tld`,
  },
  pathPrefix: "/map-turner",
  plugins: [
    {
      resolve: `gatsby-source-filesystem`,
      options: {
        // The unique name for each instance
        name: `data`,
        // Path to the directory
        path: `${__dirname}/src/data/`,
      },
    },
    `gatsby-transformer-csv`,
  ],
};