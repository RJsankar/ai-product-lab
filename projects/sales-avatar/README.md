# Sales Avatar

Sales Avatar helps sales reps practice realistic customer conversations before high-stakes meetings.

## V0.1 experience

1. Select a persona and scenario.
2. Hold a text conversation with an AI customer.
3. End the simulation.
4. Receive a score, strengths, misses, and next-step coaching.

## Why this MVP

The first release tests the core value proposition without voice, avatars, CRM integrations, RAG, or multi-agent complexity.

## Run the working MVP

```bash
cd projects/sales-avatar/src
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Add your OpenAI API key to .env
streamlit run app.py
```

The app uses the OpenAI Responses API for the customer conversation and Structured Outputs for the final coaching rubric. Set `OPENAI_MODEL` in `.env` to use another compatible model.

## What is implemented

- Three selectable customer personas
- Custom scenario setup
- Multi-turn text simulation
- Dynamic questions and objections
- End-simulation control
- Structured 1-5 rubric, strengths, misses, and next steps
- Local API-key configuration; secrets are not committed

## Project docs

- [Product brief](product-brief.md)
- [Architecture](architecture.md)
- [Evaluation plan](evals.md)

## Roadmap

- **V0.1:** Working text simulation and structured feedback
- **V0.2:** Dynamic objections
- **V0.3:** Structured evaluation output
- **V0.4:** Improved interface
- **V0.5:** Multiple personas
- **V1:** Tools, RAG, voice, and agentic behavior where valuable
