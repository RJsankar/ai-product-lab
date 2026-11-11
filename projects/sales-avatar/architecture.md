# Architecture

## V0.1 flow

```text
User -> Chat UI -> Persona prompt -> LLM -> Conversation
                                      |
                              End simulation
                                      |
                         Evaluation prompt -> Score + feedback
```

## Product choices

- **One model:** keeps cost, latency, and debugging simple.
- **Two prompts:** one runs the persona; one evaluates the completed transcript.
- **Session state:** stores the scenario and conversation history.
- **No orchestration framework:** unnecessary until the MVP proves value.

## Key risks

- Persona breaks character
- Objections feel repetitive or unrealistic
- Feedback is generic or inconsistent
- Long sessions increase latency and cost
