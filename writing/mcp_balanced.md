# Making Sense of Model Completion Protocol (MCP): Potential and Pitfalls

The Model Completion Protocol (MCP) has been generating significant buzz in the AI community lately, with strong opinions on both sides. Is it a revolutionary standard or just another layer of unnecessary abstraction? After reflecting on my experience with tool-calling implementations, I want to share my thoughts on what MCP is trying to accomplish, where it might succeed, and where it falls short.

• • •

## What Exactly Is MCP?

At its core, MCP is an attempt to standardize how language models interact with external tools and services. If you've worked with function calling in OpenAI's models or tool use in Claude, you're already familiar with the basic concept - allowing LLMs to invoke external functions to accomplish tasks they can't handle alone.

The key difference with MCP is that it aims to create a universal protocol that works across different model providers and tools, turning what was previously an M×N problem (each of M models needing custom integration with each of N tools) into an M+N problem (each model and tool only needs to implement the MCP standard once).

This is conceptually similar to how USB standardized device connections - we didn't strictly *need* it to connect peripherals, but having a standard made everything significantly easier.

## The Case For MCP

The strongest argument for MCP is the rapid adoption we're seeing across the ecosystem. Every major provider has either added support or is working on it - Anthropic, Google, OpenAI - alongside tooling companies like Docker, Postman, Zapier, and GitHub.

This level of industry buy-in suggests MCP is addressing a real pain point. For developers building on multiple LLM platforms, having a consistent way to implement tool calling could significantly reduce development overhead and maintenance burden.

IMHO, this kind of standardization is particularly valuable in a rapidly evolving field where APIs and capabilities are constantly changing. Having some stability in how we connect models to external tools provides a foundation for more complex applications.

## The Case Against MCP

MCP is essentially "a super naive RPC protocol that can only be invoked by an LLM and its tokens, and exposes exactly nothing of the host application itself."

This creates two significant limitations:

1. **Inefficiency for production apps**: Why add a poor RPC layer when you can just call a function directly? Each function call is "pressing data through an expensive unreliable needle hole" - namely, through the LLM's inference process.

2. **Limited extensibility**: MCP currently doesn't provide rich ways to extend LLM applications beyond "give me tokens the LLM thinks you should give me." It doesn't address more complex integration needs.

There's also legitimate concern about the control flow - who's actually "in the driver's seat" in an MCP implementation? Is it the LLM, the host application, or something else? This ambiguity creates confusion about how to properly structure applications.

Having the LLM be the boss seems destined to have everything pay an inference cost.

## The Historical Pattern We're Repeating

MCP feels like we're reinventing wheels without awareness of computing history. The comparison to SOAP (Simple Object Access Protocol) and CORBA (Common Object Request Broker Architecture) is particularly apt. Both were attempts to standardize how different systems communicate, and both eventually gave way to simpler, more flexible approaches.

I believe MCP will gradually add "profiles" for different use cases, schema catalogs, discovery mechanisms, capability negotiation, and special formatting tags - eerily familiar to anyone who lived through previous standardization efforts. We may be watching the birth of "SOAP for AI" or "CORBA for LLMs."

## The Control Flow Problem

A particularly thorny issue with MCP is determining the control flow between components. In current implementations like Claude Desktop, the LLM often acts as the primary controller, deciding when to call tools. But this creates inefficiencies since every interaction requires passing through the inference process.

Alternative approaches might put a Python process or the host application in control, with the LLM acting more like a coroutine that's invoked when needed. This could be more efficient but adds complexity in keeping state synchronized between components.

The current MCP implementations also have practical limitations. You can't toggle tools on and off in Claude, and you have to restart the app to refresh the server list.

## Different Use Cases Need Different Solutions

Part of the challenge is that "LLM applications" encompasses a wide range of products with different needs:

- Chat interfaces like Claude Desktop with conversation history and file attachments
- Code editors like Cursor with semantic information about codebases
- Domain-specific tools with custom knowledge and capabilities

Each of these might need different integration patterns beyond what a single protocol can provide. The "one size fits all" approach of current MCP implementations may be too limiting for specialized applications.

• • •

## Where Do We Go From Here?

MCP is clearly addressing a real need for standardization in the LLM ecosystem. The rapid adoption by major players suggests it's filling an important gap. However, the current implementation has significant limitations that shouldn't be ignored.

My prediction is that we'll see MCP evolve in one of two directions:

1. **Expansion into a more comprehensive framework** - Adding the profiles, schema catalogs, and capability negotiation that critics are already predicting, potentially becoming more complex but more powerful.

2. **Simplification into core patterns** - Distilling down to the essential patterns that work well across implementations, with extensions handled through complementary standards rather than expanding the core protocol.

For developers building LLM applications today, my advice is pragmatic: use MCP where it makes sense for cross-platform compatibility, but don't force it where direct function calling would be simpler and more efficient. Be particularly cautious about making the LLM the primary controller of your application flow if inference costs or latency are concerns.

• • •

P.S. I find it fascinating how we keep reinventing similar patterns across computing generations. The tension between standardization and flexibility is a constant in our field. MCP is just the latest chapter in this ongoing story, and watching how it evolves will be instructive regardless of whether it succeeds or fails.
