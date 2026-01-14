"""
06_webhooks.py - Implement webhooks for event-driven architecture
"""

webhook_guide = """
WEBHOOKS GUIDE:

What are Webhooks?
- HTTP callbacks for events
- Real-time notifications
- Event-driven architecture

Supported Events:
- fine_tuning.job.completed
- fine_tuning.job.failed
- batch.completed
- batch.failed

Setup:
1. Create webhook endpoint (your server)
2. Register endpoint with OpenAI
3. Verify webhook signatures
4. Handle events

Example Webhook Handler (Flask):

from flask import Flask, request
import hmac
import hashlib

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Get signature from header
    signature = request.headers.get('X-OpenAI-Signature')

    # Verify signature
    secret = os.getenv('WEBHOOK_SECRET')
    computed_sig = hmac.new(
        secret.encode(),
        request.data,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(signature, computed_sig):
        return 'Invalid signature', 401

    # Process event
    event = request.json
    event_type = event['type']

    if event_type == 'fine_tuning.job.completed':
        handle_fine_tune_complete(event)
    elif event_type == 'batch.completed':
        handle_batch_complete(event)

    return 'OK', 200

Security:
- Always verify signatures
- Use HTTPS only
- Implement idempotency
- Handle duplicates
- Log all events

Best Practices:
- Process events asynchronously
- Implement retry logic
- Return 200 quickly
- Don't do heavy processing in handler
- Use queues for processing
"""

print(webhook_guide)
