# Frequently Asked Questions (FAQ)

## General Questions

### Q: Who is this course for?
**A**: This course is designed for beginners to advanced developers who want to build applications with OpenAI's APIs. No prior AI experience is required for beginners, but basic Python knowledge is recommended.

### Q: How long does it take to complete the course?
**A**:
- **Beginners**: 20-30 hours (complete path)
- **Intermediate**: 15-20 hours (focused modules)
- **Advanced**: 10-15 hours (specialized topics)

### Q: Do I need to complete modules in order?
**A**: Yes, for beginners. Modules 1-3 build foundational knowledge. Intermediate and advanced users can skip ahead based on their experience.

### Q: Is this course free?
**A**: The course materials are provided, but you'll need your own OpenAI API key. API usage costs apply based on OpenAI's pricing.

---

## Getting Started

### Q: How do I get an OpenAI API key?
**A**:
1. Visit https://platform.openai.com/signup
2. Create an account
3. Navigate to API Keys section
4. Click "Create new secret key"
5. Copy and securely store the key

### Q: How much will API usage cost?
**A**: Costs vary by model and usage:
- **GPT-3.5-turbo**: ~$0.50-1.50 per 1M tokens
- **GPT-4**: ~$30-60 per 1M tokens
- Most examples in this course cost pennies

For the complete course, expect to spend $5-20 in API costs.

### Q: Can I use a free trial?
**A**: OpenAI offers free trial credits for new accounts. Check https://platform.openai.com/account/billing for current offers.

### Q: What if I get an authentication error?
**A**: Common causes:
1. API key not set in environment
2. Typo in API key
3. API key expired or revoked
4. Missing `.env` file

Run `verify_setup.py` from Module 1 to diagnose issues.

---

## Technical Questions

### Q: Which Python version should I use?
**A**: Python 3.8 or higher. Python 3.10+ is recommended for best compatibility.

### Q: Do I need a GPU for this course?
**A**: No. All computations happen on OpenAI's servers. You only need a basic computer with internet access.

### Q: Can I use a different programming language?
**A**: While this course uses Python, OpenAI has official SDKs for:
- JavaScript/TypeScript
- C#/.NET

The concepts translate across languages.

### Q: How do I handle rate limits?
**A**:
1. Implement exponential backoff (covered in Module 2)
2. Use batch processing for large jobs (Module 5)
3. Upgrade your usage tier
4. See Module 4 for comprehensive strategies

### Q: Why am I getting timeout errors?
**A**:
- Check your internet connection
- Increase timeout in API calls
- Use streaming for long responses
- Check OpenAI status page

### Q: How do I reduce API costs?
**A**:
1. Use GPT-3.5-turbo instead of GPT-4 when possible
2. Set `max_tokens` limits
3. Cache responses
4. Use batch processing (50% savings)
5. Trim conversation history

---

## Module-Specific Questions

### Module 1: Setup

**Q: Where should I store my API key?**
**A**: In a `.env` file that's added to `.gitignore`. Never hardcode it in your source code.

**Q: What if verify_setup.py fails?**
**A**: Check:
1. API key is correct
2. `.env` file exists
3. python-dotenv is installed
4. Internet connection works
5. OpenAI service is up

### Module 2: Getting Started

**Q: What's the difference between GPT-3.5 and GPT-4?**
**A**:
- **GPT-3.5-turbo**: Faster, cheaper, good for most tasks
- **GPT-4**: More capable, better reasoning, higher cost

Use GPT-3.5 for development and simple tasks, GPT-4 for complex reasoning.

**Q: How do I make my chatbot remember context?**
**A**: Maintain conversation history and send it with each request. See `06_simple_chatbot.py` for implementation.

### Module 3: Core Concepts

**Q: Can GPT-4 Vision analyze videos?**
**A**: Not directly. You can extract frames and analyze them as images, or use OpenAI's video API when available.

**Q: What audio formats does Whisper support?**
**A**: mp3, mp4, mpeg, mpga, m4a, wav, webm, up to 25 MB

**Q: How do I generate images with DALL-E?**
**A**: Use `client.images.generate()` with a text prompt. See `06_image_generation.py` for examples.

### Module 4: API Reference

**Q: How often should I rotate API keys?**
**A**: Recommended every 90 days, or immediately if compromised.

**Q: Can I use the same key across environments?**
**A**: Not recommended. Use separate keys for dev, staging, and production.

### Module 5: Platform APIs

**Q: When should I fine-tune a model?**
**A**: When:
- You have 50+ quality examples
- Domain-specific terminology is needed
- Consistent output format is required
- Prompting alone doesn't achieve desired results

**Q: How long does fine-tuning take?**
**A**: Typically minutes to hours depending on dataset size. You'll receive webhook notifications.

**Q: What's the difference between embeddings models?**
**A**:
- `text-embedding-3-small`: Fast, efficient, good for most use cases
- `text-embedding-3-large`: Highest quality, more expensive

---

## Troubleshooting

### Q: I'm getting "Invalid API key" errors
**A**:
1. Verify key starts with `sk-`
2. Check for extra spaces/newlines
3. Ensure key isn't revoked
4. Try generating a new key

### Q: Requests are very slow
**A**:
1. Check OpenAI status page
2. Use faster models (GPT-3.5-turbo vs GPT-4)
3. Reduce `max_tokens`
4. Use streaming for immediate feedback

### Q: I'm hitting rate limits constantly
**A**:
1. Implement exponential backoff
2. Upgrade usage tier
3. Use batch processing
4. Spread requests over time
5. Cache common responses

### Q: Token counts are higher than expected
**A**: Remember:
- Conversation history counts toward tokens
- System messages count
- Function definitions count
- Each message has overhead (~4 tokens)

### Q: Function calling isn't working
**A**: Check:
1. Function schema is valid JSON Schema
2. Required parameters are specified
3. Using a model that supports functions
4. `tool_choice` is set appropriately

---

## Best Practices

### Q: Should I use temperature 0 or 1?
**A**: Depends on use case:
- **0-0.3**: Focused, deterministic (Q&A, data extraction)
- **0.7-0.9**: Balanced (chatbots, general use)
- **1.0-2.0**: Creative (content generation, brainstorming)

### Q: How many examples for few-shot prompting?
**A**: Usually 2-5 examples is optimal. More isn't always better.

### Q: Should I use function calling or structured outputs?
**A**:
- **Function calling**: When you need to trigger actions
- **Structured outputs**: When you need specific data format

### Q: How do I prevent API key exposure?
**A**:
1. Use environment variables
2. Add `.env` to `.gitignore`
3. Never commit keys to version control
4. Use key scanning tools (e.g., git-secrets)
5. Rotate keys if exposed

---

## Advanced Topics

### Q: How do I build a production-grade chatbot?
**A**: Key components:
1. Conversation state management
2. Error handling with retries
3. Rate limiting
4. Content moderation
5. Logging and monitoring
6. Cost tracking
7. Caching layer

See Module 8 for complete guide.

### Q: What's the best way to do semantic search?
**A**:
1. Create embeddings for your documents
2. Store in vector database (Pinecone, Weaviate, pgvector)
3. Embed user query
4. Find similar vectors
5. Return relevant documents

See Module 5 for implementation.

### Q: How do I evaluate my AI application?
**A**:
1. Define success metrics
2. Create test dataset
3. Run evaluations regularly
4. Compare model versions
5. Use OpenAI's Evals framework

Covered in Module 7.

---

## Billing and Pricing

### Q: How is API usage billed?
**A**: By tokens:
- **Input tokens**: Your prompts and conversation history
- **Output tokens**: AI-generated responses

Check current pricing at https://openai.com/pricing

### Q: Can I set spending limits?
**A**: Yes, in your OpenAI account:
1. Go to Settings > Billing
2. Set usage limits
3. Configure alerts

### Q: What's the cheapest way to use OpenAI?
**A**:
1. Use GPT-3.5-turbo for most tasks
2. Set `max_tokens` limits
3. Use batch processing (50% cheaper)
4. Cache responses
5. Trim conversation history

### Q: Do I pay for failed requests?
**A**: No. You only pay for successful completions.

---

## Course Support

### Q: I found an error in the course. How do I report it?
**A**: Create an issue on the GitHub repository with:
- Module and file name
- Description of the error
- Expected vs actual behavior

### Q: Can I contribute to the course?
**A**: Yes! Contributions are welcome:
- Fix typos or errors
- Add examples
- Improve explanations
- Share projects built with the course

### Q: Where can I get help with my code?
**A**:
1. Review the relevant module
2. Check the FAQ (this document)
3. Search OpenAI community forum
4. Review OpenAI documentation
5. Ask in developer communities

### Q: Are there video tutorials?
**A**: This course is text and code-based. For video tutorials, check:
- OpenAI YouTube channel
- Community-created content

---

## Staying Updated

### Q: How often is this course updated?
**A**: Periodically to reflect:
- New OpenAI features
- API changes
- Best practice updates
- Community feedback

### Q: Where can I learn about new OpenAI features?
**A**:
- OpenAI Changelog: https://platform.openai.com/docs/changelog
- OpenAI Blog: https://openai.com/blog
- Developer forum: https://community.openai.com/

### Q: Will my code break when OpenAI updates?
**A**: OpenAI maintains backward compatibility for API v1. However:
- Pin model versions in production
- Test before upgrading
- Monitor changelog

---

## Additional Resources

### Q: What are the best resources beyond this course?
**A**:
- **Official Docs**: https://platform.openai.com/docs
- **Cookbook**: https://github.com/openai/openai-cookbook
- **Community Forum**: https://community.openai.com/
- **Research Papers**: https://openai.com/research
- **YouTube**: OpenAI official channel

### Q: Are there communities I can join?
**A**:
- OpenAI Developer Forum
- Reddit: r/OpenAI
- Discord: Various AI/ML servers
- Twitter: #OpenAI hashtag

### Q: What should I build to practice?
**A**: Start with:
1. Personal chatbot with memory
2. Document Q&A system
3. Code assistant
4. Content generator
5. Image analyzer

Then progress to module 9 projects.

---

## Still Have Questions?

If your question isn't answered here:
1. **Check the course modules** - Most topics are covered in depth
2. **Search the OpenAI docs** - Comprehensive API documentation
3. **Visit the forum** - https://community.openai.com/
4. **Review examples** - OpenAI Cookbook has many examples

---

**Last Updated**: January 2026
**Course Version**: 1.0.0
