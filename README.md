# SyntaxPilot: Verified Code Completion

## Overview

**SyntaxPilot** is an AI-assisted code autocompletion tool that leverages a fine-tuned GPT-2 model in combination with formal language verification using Lex and Bison. It provides intelligent code suggestions while filtering out syntax-invalid outputs using a formal grammar checker, ensuring only valid code suggestions reach the user.

---

## Features

- **LLM-Powered Code Suggestions**: Fine-tuned GPT2-small on the Postgres C codebase.
- **Syntax Validation**: All completions are checked using a Lex and Bison grammar before being shown.
- **Single-Line Irrecoverable Syntax Error Detection**: Verifies and filters out invalid suggestions like `for(int i=;;{`.
- **IDE Integration**: Simple UI extension for IntelliJ to access predictions and view valid completions.

---

## Architecture

- **Tokenizer**: Simple splitter-based tokenizer to maintain context fidelity, feeding directly into the LLM.
- **Language Model**: GPT2-small fine-tuned on ~55K cleaned C code samples from the Postgres source.
- **Verification Layer**: Lex converts completions into token categories → Bison uses CFG to verify syntax validity.
- **Interface**: IntelliJ plugin displays suggestions upon request with backend script coordination.

---

## How It Works

1. **User types code** → Suggestion request sent to backend.
2. **LLM generates completion** based on context using fine-tuned GPT2.
3. **Lex & Bison validate** the completion line for syntactic soundness.
4. **Only valid completions** are returned to the user in IntelliJ.

---

## Setup Instructions

### Requirements

- Python 3.10+
- Lex & Bison (GNU tools)
- Java + IntelliJ IDEA (for extension)
- `transformers` library
- `datasets` for pre-processing (optional for retraining)
