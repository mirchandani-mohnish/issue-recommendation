const Octokit = require('octokit');

const octokit = new Octokit({ 
  auth: process.env.TOKEN,
});

octokit.request("GET /octocat", {});
