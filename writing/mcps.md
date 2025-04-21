MCPs: A Solution in Search of a Problem

Model Control Protocol (MCP) has emerged as one of those technologies that's generating buzz in AI circles, but when you look under the hood, there are legitimate questions about what problem it's actually solving. Having spent time examining its architecture and intended use cases, I've developed some thoughts on why it might represent a case of putting the cart before the historical horse.

# A Historical Perspective

What's particularly interesting about the MCP situation is how it reflects a pattern we've seen repeatedly in software engineering: the tendency to create new abstractions without fully understanding the problem space or examining historical solutions.

We've seen similar patterns with:
- SOAP web services in the early 2000s
- Enterprise Service Buses (ESBs)
- Various middleware solutions
- Early microservice architectures

Each of these went through periods of hype, overengineering, and eventually simplification as real-world requirements became clearer.

# The Fundamental Disconnect

MCPs are essentially trying to solve a problem that many practitioners don't recognize as a problem in the first place. This disconnect creates immediate friction in adoption and understanding in production environments

IMHO, what we're seeing is a classic case of relatively young engineers (mostly under 30) tackling complex system integration challenges without sufficient awareness of historical approaches to similar problems. This isn't a criticism of their abilities, but rather an observation that we might be reinventing wheels that have already gone through several evolutionary cycles.

At its core, MCP aims to be a mechanism for extending LLM-powered applications. But what we've ended up with is essentially a naive Remote Procedure Call (RPC) protocol with two significant limitations:

1. It can only be invoked by an LLM and its tokens
2. It exposes virtually nothing of the host application itself

This creates a fundamental architectural problem. For production applications, why would developers add a poor RPC layer when they could just call a function directly? The value proposition simply isn't there. And for real-world use cases, each function call forces data through what I'd describe as an expensive, unreliable needle hole – the LLM inference process.

# The Inevitable Evolution Cycle

I can already see where this is headed. Before long, we'll start seeing proposals for "profiles" – perhaps a "code editor profile" that provides arbitrary data from the conversation context, or a "chat bot profile" with its own specialized capabilities.

Then the natural progression:
- We'll define schema catalog mechanisms
- Add discovery mechanisms for profiles
- Create systems for negotiating capabilities
- Eventually add XML-style tags (because Anthropic already trains their models that way)
- And finally, we'll rebrand it as something like Standard Operating AI Protocol (SOAP) or Common Operating Recipe for Building AI (CORBA)

If those acronyms sound familiar, it's because we've been down similar roads before in software architecture. The parallels to historical protocol evolutions like SOAP and CORBA aren't accidental – they represent similar attempts to solve integration challenges that eventually became overly complex.

# Who's in The Driver's Seat

There's another dimension to this that's worth exploring: who exactly is "in the driver's seat" in an MCP architecture? Currently, it seems the MCP host (like Claude Desktop) takes this position by default, which makes sense given current incentives for MCP server authors and frontier model labs.

But my intuition suggests that a "vanilla" Python process might actually be a better long-term driver. This would require figuring out the sequencing and control flow between the LLM and the Python process, but it would remove the constraint of "run it through inference by default" that current architectures impose.

Perhaps the ideal "driver" should have lifecycle hooks into every tool use, including:
- The ability to transform inputs from the LLM prior to tools being called
- The ability to transform outputs before being read by the model as context

This would come at the cost of increased complexity in the joint programming model (driver, LLM, tool) and the challenge of keeping all state synchronized – but might ultimately provide more flexibility and control.

# Looking Forward

So where does this leave us with MCPs? I'm not suggesting they have no value – they clearly represent an attempt to solve real integration challenges in the LLM space. But I do think we need to be more thoughtful about whether they're the right solution for the problems we're actually facing.

Some questions worth considering:
- What are the actual integration challenges that can't be solved with direct function calls?
- How can we leverage existing, battle-tested integration patterns?
- Are we optimizing for the right constraints (developer experience, performance, flexibility)?

The AI ecosystem is evolving rapidly, and it's natural that we'll try different approaches to integration. But as we do, let's make sure we're learning from software history rather than being doomed to repeat it.

What do you think? Have you worked with MCPs in production? I'd be curious to hear about real-world experiences and whether they're solving genuine problems or creating new ones.
