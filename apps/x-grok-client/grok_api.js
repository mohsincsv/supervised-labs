const express = require('express');
const rateLimit = require('express-rate-limit');
const { loadSecrets } = require('./utils/loadEnv');
const secrets = require('./utils/secrets');
const AccountManager = require('./utils/accountManager');

const app = express();
let accountManager = null;

app.use(express.json());

let grokLimiter;

app.post('/grok-chat', (req, res, next) => {
    if (grokLimiter) {
        grokLimiter(req, res, next);
    } else {
        console.error("grokLimiter was not initialized before request to /grok");
        res.status(500).json({ error: 'Internal Server Error: Rate limiter not configured.' });
    }
}, async (req, res, next) => {
  console.log('Received /grok request with payload:', JSON.stringify(req.body, null, 2));
  if (!accountManager) {
    console.error('/grok: AccountManager not initialized.');
    return res.status(503).json({ error: 'Service unavailable. Account manager not initialized.' });
  }
  const activeAccount = accountManager.getActiveScraper();
  if (!activeAccount || !activeAccount.scraper) {
    console.warn('/grok: No active scraper available from AccountManager.');
    return res.status(503).json({ error: 'Service temporarily unavailable. All accounts might be in cooldown or facing issues.' });
  }
  const scraperInstance = activeAccount.scraper;

  const { messages, conversationId, returnSearchResults, returnCitations, mode, modelId } = req.body;
  if (!messages || !Array.isArray(messages) || messages.length === 0) {
      console.warn('Received /grok request with missing or invalid messages array.');
      return res.status(400).json({ error: 'Missing or invalid "messages" array in request body.' });
  }

  const validModes = ['regular', 'deepsearch', 'deepsearch_deeper', 'think'];
  const validatedMode = mode && validModes.includes(mode) ? mode : 'regular';
  const validatedModelId = typeof modelId === 'string' && modelId.trim() !== '' ? modelId.trim() : undefined;

  try {
    console.log(`Using account: ${activeAccount.credentials.username} for /grok request. Mode: ${validatedMode}${validatedModelId ? `, ModelID: ${validatedModelId}` : ''}`);
    const grokResponse = await scraperInstance.grokChat({
      messages,
      conversationId,
      returnSearchResults: returnSearchResults || false,
      returnCitations: returnCitations || false,
      mode: validatedMode,
      modelId: validatedModelId,
    });

    accountManager.incrementRequestCount(activeAccount.id); // Increment count on success
    console.log(`Successfully received response from grokChat via ${activeAccount.credentials.username}. Conversation: ${grokResponse.conversationId}`);
    res.status(200).json(grokResponse);

  } catch (error) {
    console.error(`Error during grokChat for account ${activeAccount.credentials.username}:`, error.message);
    next(error);
  }
});


// --- Start Server Function ---
function startServer() {
  const port = secrets.PORT;
  console.log(`Attempting to start server on port ${port}...`);
  app.listen(port, () => {
    console.log(`✅ Server listening on port ${port}`);
    if (accountManager) {
        const readyScrapersCount = accountManager.accounts.filter(a => a.isReady).length;
        if (readyScrapersCount === 0 && accountManager.accounts.length > 0) {
            console.warn('⚠️ Warning: Server started, but no scraper accounts are ready. Health check will report error.');
        } else if (accountManager.accounts.length === 0) {
            console.warn('⚠️ Warning: Server started, but no scraper accounts are configured.');
        }
    } else {
         console.warn('⚠️ Warning: Server started, but AccountManager is not initialized.');
    }
  }).on('error', (err) => {
      console.error(`❌ Failed to start server on port ${port}:`, err);
      process.exit(1);
  });
}

// --- Graceful Shutdown Handling ---
const signals = { 'SIGINT': 2, 'SIGTERM': 15 };
Object.keys(signals).forEach((signal) => {
  process.on(signal, async () => {
    console.log(`Received ${signal} signal. Preparing to exit...`);
    console.log('Shutdown complete.');
    process.exit(128 + signals[signal]);
  });
});

process.on('uncaughtException', (err, origin) => {
    console.error('FATAL: Uncaught exception detected:', err, 'Origin:', origin);
    process.exit(1);
});

process.on('unhandledRejection', (reason, promise) => {
    console.error('FATAL: Unhandled promise rejection detected:', reason, 'Promise:', promise);
    process.exit(1);
});


// --- Main Application Start ---
async function main() {
    try {
        // 1. Load Secrets
        console.log('Loading configuration...');
        await loadSecrets();
        console.log('✅ Configuration loaded successfully.');

        // 2. Initialize AccountManager
        console.log('Initializing AccountManager...');
        accountManager = new AccountManager(); // Create instance
        await accountManager.initializeScrapers(); // Initialize all scrapers
        // initializeScrapers() already logs success/failure details.

        // 3. Configure middleware dependent on secrets (e.g., rate limiter for incoming IP)
        console.log('Configuring middleware (IP rate limiter)...');
         grokLimiter = rateLimit({
            windowMs: secrets.RATE_LIMIT_WINDOW_MS,
            max: secrets.RATE_LIMIT_MAX,
            standardHeaders: true,
            legacyHeaders: false,
            message: { error: 'Too many requests from this IP, please try again later.' },
             keyGenerator: (req) => req.ip,
             handler: (req, res, next, options) => {
                console.warn(`IP Rate limit exceeded for IP: ${req.ip}`);
                 res.status(options.statusCode).send(options.message);
             }
        });
        console.log('✅ IP Rate Limiter middleware configured.');

        // 4. Start Server
        startServer();

    } catch (error) {
        console.error('❌ Fatal error during application startup:', error);
        process.exit(1);
    }
}

// Start the application
main();
