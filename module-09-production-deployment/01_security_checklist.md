# 🔒 OpenAI Production Security Checklist

## 1. API Key Management
- [ ] **Environment Variables**: Store keys in `.env` (python-dotenv) or secrets manager (AWS Secrets, Vault).
- [ ] **No Hardcoding**: Scan code for sk-... patterns before commit.
- [ ] **Project-Scoped Keys**: Use separate keys for Dev, Staging, and Prop.
- [ ] **Spend Limits**: Set hard/soft limits in the OpenAI Dashboard to prevent billing runaway.

## 2. Input Validation (Prompt Injection)
- [ ] **Input Length Limits**: Restrict user input character count to prevent context exhaustion attacks.
- [ ] **Delimiters**: Wrap user input in XML tags (e.g., `<user_input>{input}</user_input>`) to separate it from instructions.
- [ ] **Indirect Injection**: Treat data from external sources (emails, websites) as untrusted.

## 3. Output Handling
- [ ] **Sanitization**: If rendering HTML/Markdown from AI, sanitize for XSS.
- [ ] **Guardrails**: Use a secondary check (regex or cheap model) to verify output doesn't contain forbidden content.

## 4. Data Privacy
- [ ] **Zero Data Retention**: If applicable, set `Zero Data Retention` policies in enterprise settings.
- [ ] **PII Scrubbing**: Remove emails/phones before sending to API if not needed.

## 5. Reliability
- [ ] **Timeouts**: Always set a timeout on API calls (default is infinite/very long).
- [ ] **Fallbacks**: Handle 500/503 errors gracefully (exponential backoff).
