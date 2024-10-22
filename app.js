const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');
const { PythonShell } = require('python-shell');

// Initialize the Express app
const app = express();
const port = 3000;

// Serve the static files from 'public' directory
app.use(express.static(path.join(__dirname, 'public')));
app.use(bodyParser.json());

// API endpoint for fuzzy search
app.post('/search', (req, res) => {
    const query = req.body.query;

    if (!query) {
        return res.status(400).json({ error: 'Query is missing' });
    }

    // Call the Python script with the query
    const options = {
        mode: 'json',
        pythonOptions: ['-u'],  // Enable unbuffered output for real-time prints
        args: [query]  // Pass the search query to the Python script
    };

    PythonShell.run('fuzzy_search.py', options, (err, results) => {
        if (err) {
            console.error('Error running Python script:', err);
            return res.status(500).json({ error: 'Fuzzy search failed' });
        }

        // Send the results from Python to the client
        res.json(results);
    });
});

// Start the server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
