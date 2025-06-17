// This is a simple Node.js Express server to act as a proxy for the Gemini API.
// To run this, you would need Node.js installed.
// 1. Save this file as server.js
// 2. In your terminal, run `npm install express node-fetch`
// 3. Set your API key as an environment variable: `export API_KEY="YOUR_API_KEY"`
// 4. Run the server: `node server.js`
// Your index.html file will then be able to make requests to this server instead of directly to Google.

const express = require('express');
const fetch = require('node-fetch');
const app = express();
app.use(express.json());

const API_KEY = process.env.API_KEY;
const API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent';

// Proxy endpoint for strategy analysis
app.post('/api/analyze', async (req, res) => {
    try {
        const { prompt } = req.body;
        const payload = {
            contents: [{ role: "user", parts: [{ text: prompt }] }]
        };

        const response = await fetch(`${API_URL}?key=${API_KEY}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        const data = await response.json();
        
        if (data.candidates && data.candidates.length > 0) {
            let text = data.candidates[0].content.parts[0].text;
            text = text.replace(/```html|```/g, '');
            res.json({ text });
        } else {
            res.status(500).json({ error: 'No response from AI model', details: data });
        }
    } catch (error) {
        console.error('Error in /api/analyze:', error);
        res.status(500).json({ error: 'Server error' });
    }
});

// Proxy endpoint for parameter suggestions
app.post('/api/suggest', async (req, res) => {
    try {
        const { prompt } = req.body;
        const schema = {
             type: "OBJECT",
            properties: {
                "shortMA": { "type": "INTEGER" },
                "longMA": { "type": "INTEGER" },
                "rsiPeriod": { "type": "INTEGER" },
                "rsiOverbought": { "type": "INTEGER" },
                "rsiOversold": { "type": "INTEGER" },
                "bbPeriod": { "type": "INTEGER" },
                "bbStdDev": { "type": "NUMBER" },
                "volumeMAPeriod": { "type": "INTEGER" },
                "stopLoss": { "type": "NUMBER" },
                "takeProfit": { "type": "NUMBER" },
                "useSLTP": { "type": "BOOLEAN" },
                "useRsiFilter": { "type": "BOOLEAN" },
                "useBBFilter": { "type": "BOOLEAN" },
                "useVolumeFilter": { "type": "BOOLEAN" }
            }
        };

        const payload = {
            contents: [{ role: "user", parts: [{ text: prompt }] }],
            generationConfig: {
                responseMimeType: "application/json",
                responseSchema: schema
            }
        };

        const response = await fetch(`${API_URL}?key=${API_KEY}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        if (data.candidates && data.candidates.length > 0) {
            let jsonText = data.candidates[0].content.parts[0].text;
            jsonText = jsonText.replace(/```json|```/g, '').trim();
            res.json(JSON.parse(jsonText));
        } else {
             res.status(500).json({ error: 'No response from AI model', details: data });
        }
    } catch (error) {
        console.error('Error in /api/suggest:', error);
        res.status(500).json({ error: 'Server error' });
    }
});

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
    console.log('Ensure your index.html is opened in a way that can access this server.');
    console.log('Remember to set your API_KEY environment variable.');
});
