# Sovereign XML Compiler

**Natural language → valid XML system prompts in one shot. Zero correction iterations.**

Three modes using logit gating at the tokenization layer:

## Modes

### 1. GBNF Constrained Decoding (best)
Uses llama.cpp grammar-based sampling. The model **physically cannot** output invalid XML.
Token selection at the softmax layer is masked to enforce the grammar.
Result: 100% valid XML, zero syntax errors, one pass.

```bash
# Requires llama.cpp server running
export LLAMA_URL=http://localhost:8080
python server/compiler.py --mode gbnf --input "You are a Lean 4 proof verifier..."
```

### 2. Skeleton In-Filling
LLM only fills `{{PLACEHOLDER}}` values. Parser injects into template.
The model never writes `<` or `>` — no tag hallucination possible.

```bash
python server/compiler.py --mode skeleton --input "You are a sovereign math agent..."
```

### 3. Dual-Pass Chain-of-XML
`<thought_process>` first, `<xml_output>` second.
Forces attention to compute correct structure before emitting markup.

```bash
python server/compiler.py --mode dual-pass --input "..."
```

## Quick Start

```bash
export OLLAMA_URL=http://localhost:11434
export XML_MODEL=nemotron

python server/compiler.py --mode skeleton \
  --input "You are a zero-sorry Lean 4 verifier. Reject any proof containing sorry." \
  --output my_prompt.xml
```

## Files

| File | Purpose |
|------|---------|
| `grammars/sovereign_prompt.gbnf` | GBNF grammar for llama.cpp constrained decoding |
| `skeletons/sovereign_prompt.xml` | XML skeleton with `{{PLACEHOLDER}}` tokens |
| `server/compiler.py` | Three-mode compiler server |

## The Gate Taxonomy

| Mode | Gate Type | Mechanism |
|------|-----------|-----------|
| GBNF | Weight-level structural gate | Token masking at softmax — invalid tokens → probability 0 |
| Skeleton | Context gate | LLM sees only leaf values, never writes tags |
| Dual-pass | Attention gate | CoT forces structure before syntax |

## Connection to Gates Normalization

GBNF masking is `P(token | grammar) = 0` for forbidden tokens.
This is the same logit gate formalism from the Gates Normalization paper:
`G_P(D_M) = softmax(logits_M + b_P)` where `b_P = -∞` for grammar-violating tokens.
The simplex constraint holds: ∑P = 1 over the valid token set.

## License
Sovereign Source License v2.0
