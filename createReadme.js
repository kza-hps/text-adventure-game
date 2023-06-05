// Define README content as a string
const readmeContent = `# Text Adventure Game

Welcome to the Text Adventure Game!

To play, simply open the game file and follow the prompts to enter text commands. GPT-3 will generate responses and descriptions based on your inputs.

Enjoy!`;

// Import the fs module to write README.md file
const fs = require('fs');

// Write README.md file
fs.writeFile('README.md', readmeContent, (err) => {
  if (err) throw err;
  console.log('README file has been created!');
});
