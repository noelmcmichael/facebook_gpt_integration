const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const config = JSON.parse(fs.readFileSync('playwright.config.json', 'utf8'));
const { baseUrl, pages, outputDir } = config;

if (fs.existsSync(outputDir)) {
  fs.rmSync(outputDir, { recursive: true, force: true });
}
fs.mkdirSync(outputDir, { recursive: true });

let hasErrors = false;
const summary = [];

for (const page of pages) {
  const url = `${baseUrl}${page.path}`;
  const pageOutputDir = path.join(outputDir, page.name);
  
  try {
    console.log(`Analyzing page: ${url}`);
    execSync(`node analyze-page.js "${url}" "${pageOutputDir}"`, { stdio: 'inherit' });
    
    const consoleLog = JSON.parse(fs.readFileSync(path.join(pageOutputDir, 'console.json'), 'utf8'));
    const errors = consoleLog.filter(msg => msg.type === 'error');
    
    if (errors.length > 0) {
      hasErrors = true;
      summary.push({ page: page.name, status: 'failed', errors });
    } else {
      summary.push({ page: page.name, status: 'passed' });
    }
  } catch (error) {
    hasErrors = true;
    summary.push({ page: page.name, status: 'failed', error: 'Test script failed to run.' });
  }
}

fs.writeFileSync(path.join(outputDir, 'summary.json'), JSON.stringify(summary, null, 2));

console.log(`\nTest run complete. Summary written to ${path.join(outputDir, 'summary.json')}`);

if (hasErrors) {
  console.error('\nErrors were found during the test run.');
  process.exit(1);
} else {
  console.log('\nNo errors found.');
  process.exit(0);
}
