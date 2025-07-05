const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const url = process.argv[2];
  const outputDir = process.argv[3];

  if (!url || !outputDir) {
    console.error('Usage: node analyze-page.js <URL> <outputDir>');
    process.exit(1);
  }

  fs.mkdirSync(outputDir, { recursive: true });

  const browser = await chromium.launch();
  const context = await browser.newContext({
    recordVideo: { dir: outputDir }
  });
  const page = await context.newPage();

  const messages = [];
  page.on('console', msg => {
    messages.push({ type: msg.type(), text: msg.text() });
  });

  try {
    await page.goto(url, { waitUntil: 'networkidle' });
    await page.screenshot({ path: path.join(outputDir, 'screenshot.png'), fullPage: true });
  } catch (error) {
    console.error(`Failed to analyze page: ${url}`, error);
    process.exit(1);
  } finally {
    const videoPath = await page.video().path();
    fs.writeFileSync(path.join(outputDir, 'console.json'), JSON.stringify(messages, null, 2));
    
    await context.close();
    await browser.close();

    fs.renameSync(videoPath, path.join(outputDir, 'video.webm'));
  }
})();
