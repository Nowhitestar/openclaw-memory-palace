# User Flow

## What the user experiences

1. The user chats with OpenClaw normally.
2. The user shares an interesting link or asks to remember something.
3. OpenClaw stores/retrieves memory behind the scenes.
4. Later, the user asks:
   - "What did we decide before?"
   - "Find that article I saved about agent memory."
   - "Why did we switch approaches?"
5. OpenClaw answers with better continuity.

## What happens internally

- OpenClaw calls the `mp` integration layer.
- The full source text is stored locally.
- Search runs against chunked semantic indexes.
- Relations can be enriched into the knowledge graph.

The key idea: **users interact with OpenClaw, not with storage internals.**
