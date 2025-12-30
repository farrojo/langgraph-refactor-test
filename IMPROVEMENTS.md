# Improvements

## 1) Brainstorming (priority)
- Fix tool step so “search_queries” produce usable research contex, a baseline generated queries but no grounded material, so revision could not improve meaningfully
- Reduce model randomness to lower drift/hallucination and improve instruction following
- Align revision prompt with available evidence (no web browsing) while still enforcing citations references
- Add early stopping based on “good enough” quality criteria to prevent endless self revision and topic drift

## 2) Why? (trigger, external reference)
Change A : Structured tool brief and citable sources
- Trigger: baseline produced search_queries but the workflow still returned a generic answer without grounded structure -> artifacts/baseline_output.txt, step 1

Change B : Lower temperature
- Trigger: the response was broad and hand-wavy, and iteration risked drifting rather than tightening the answer,baseline step 1


Change C : Grounded revision instructions -> cite only provided sources
- Trigger: revision prompt required numeric citations and URLs, but the system had no reliable retrieval step, encouraging fabricated references


Change D : Early stopping when quality criteria met
- Trigger: the workflow kept revising even after producing a strong structured answer, increasing drift and latency -> artifacts/improved_output.txt


## 3) Impact
- Tool brief and sources: improves completeness and reduces generic answers by giving the reviser actionable structure.
- Lower temperature: improves robustness and reduces hallucination/drift.
- Grounded revision prompt: reduces fabricated citations and makes references consistent
- Early stopping: improves performance -> quality per token/step and prevents runaway self revision

## 4) Next steps (2 more hours)
- Add a small evaluator that scores “coverage” (mitigation, adaptation, metrics and barriers) and uses it for termination
- Add a lightweight claim-checking pass to flag unverifiable specifics and force safer phrasing
- Expand tool output schema to a strict JSON object (parsed and validated) to avoid free-form JSON-in-string
