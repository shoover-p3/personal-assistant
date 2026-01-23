// Cloudflare Worker for Personal Assistant Slack Bot
// Receives Slack messages and writes to GitHub captures.json

export default {
  async fetch(request, env) {
    // Handle only POST requests
    if (request.method !== 'POST') {
      return new Response('Method not allowed', { status: 405 });
    }

    const body = await request.json();

    // Handle Slack URL verification challenge
    if (body.type === 'url_verification') {
      return new Response(JSON.stringify({ challenge: body.challenge }), {
        headers: { 'Content-Type': 'application/json' }
      });
    }

    // Handle message events
    if (body.type === 'event_callback' && body.event.type === 'message') {
      // Ignore bot messages to prevent loops
      if (body.event.bot_id) {
        return new Response('OK', { status: 200 });
      }

      const message = body.event.text;
      const userId = body.event.user;

      // Parse message format: "TYPE Domain: content" (optional structured format)
      // Examples: "TASK Work: Schedule meeting" or "OUTCOME Personal Growth: Read for 30 min"
      const match = message.match(/^(TASK|OUTCOME|NOTE|PROJECT)\s+([^:]+):\s*(.+)$/i);

      let capture;

      if (match) {
        // Structured format
        const [, type, domain, content] = match;
        capture = {
          timestamp: new Date().toISOString(),
          type: type.toLowerCase(),
          domain: domain.trim(),
          content: content.trim(),
          processed: false
        };
      } else {
        // Unstructured format - capture raw message for processing during check-in
        capture = {
          timestamp: new Date().toISOString(),
          type: "raw",
          domain: null,
          content: message.trim(),
          processed: false
        };
      }

      // Write to GitHub
      try {
        await appendToGitHubCaptures(env.GITHUB_TOKEN, capture);
        if (capture.type === "raw") {
          await sendSlackMessage(env.SLACK_BOT_TOKEN, body.event.channel,
            `✓ Captured for review during check-in`);
        } else {
          await sendSlackMessage(env.SLACK_BOT_TOKEN, body.event.channel,
            `✓ Captured: ${capture.type} in ${capture.domain}`);
        }
      } catch (error) {
        console.error('Error writing to GitHub:', error);
        await sendSlackMessage(env.SLACK_BOT_TOKEN, body.event.channel,
          `✗ Failed to capture: ${error.message}`);
      }
    }

    return new Response('OK', { status: 200 });
  }
};

// Append capture to GitHub captures.json
async function appendToGitHubCaptures(token, capture) {
  const owner = 'shoover-p3';
  const repo = 'personal-assistant';
  const path = 'data/captures.json';
  const branch = 'master';

  // Get current file
  const getUrl = `https://api.github.com/repos/${owner}/${repo}/contents/${path}?ref=${branch}`;
  const getResponse = await fetch(getUrl, {
    headers: {
      'Authorization': `token ${token}`,
      'Accept': 'application/vnd.github.v3+json',
      'User-Agent': 'Personal-Assistant-Bot'
    }
  });

  let sha = null;
  let captures = { captures: [] };

  if (getResponse.ok) {
    const data = await getResponse.json();
    sha = data.sha;
    const content = atob(data.content);
    captures = JSON.parse(content);
  }

  // Append new capture
  captures.captures.push(capture);

  // Commit updated file
  const updateUrl = `https://api.github.com/repos/${owner}/${repo}/contents/${path}`;
  const updateResponse = await fetch(updateUrl, {
    method: 'PUT',
    headers: {
      'Authorization': `token ${token}`,
      'Accept': 'application/vnd.github.v3+json',
      'User-Agent': 'Personal-Assistant-Bot',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      message: `Add capture: ${capture.type} in ${capture.domain}`,
      content: btoa(JSON.stringify(captures, null, 2)),
      sha: sha,
      branch: branch
    })
  });

  if (!updateResponse.ok) {
    const error = await updateResponse.text();
    throw new Error(`GitHub API error: ${error}`);
  }
}

// Send message to Slack
async function sendSlackMessage(token, channel, text) {
  await fetch('https://slack.com/api/chat.postMessage', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      channel: channel,
      text: text
    })
  });
}
