# 🦇 LangGraph Email Classifier Agent

A pure-code, intelligent email classification and automated routing agent built using **LangGraph**, **OpenRouter (Qwen)**, and **Pydantic**. This agent autonomously analyzes incoming email content, determines its priority/category, evaluates confidence levels, generates concise summaries, and executes appropriate routing actions (such as high-priority alerts).

---

## 🚨 1. Problem
Manual email handling is inefficient, and critical client or system issues risk being missed in high-volume inboxes. Processing unstructured text directly and mapping it dynamically to automated execution actions (like urgent alerts or routine sorting) is difficult using traditional LLM text responses alone, as they lack structured state control.

---

## 📐 2. Graph Diagram (LangGraph Workflow Architecture)

The logical execution flow of the agent's state graph:

```text
       +-------------------------+
       |       [ START ]         |
       +-------------------------+
                    |
                    v
       +-------------------------+
       |   classify_email_node   |  <-- LLM Call via OpenRouter (Qwen)
       +-------------------------+       & Pydantic Structured Output
                    |
                    v
       +-------------------------+
       |   Conditional Edge      |  <-- Priority Check (urgent / work / spam)
       +-------------------------+
         /          |          \
        /           |           \
       v            v            v
+------------+ +------------+ +------------+
| urgent_node| |  work_node | |  spam_node |
+------------+ +------------+ +------------+
       \            |            /
        \           |            /
         v          v          v
       +-------------------------+
       |        [ END ]          |
       +-------------------------+


 🎯 3. Key Learnings
 
Deterministic Routing: Mastered the implementation of LangGraph's StateGraph and conditional edges to guide non-deterministic LLM outputs into predictable code execution paths.

Structured Schema Validation: Enforced strict Pydantic data models alongside OpenRouter's qwen/qwen-2.5-72b-instruct to guarantee 100% type-safe JSON responses (category, confidence, summary, reasoning).

Secure Environment Isolation: Implemented clean Git tree tracking and .env secret protection protocols to prevent accidental API key leaks in version control history.

⚠️ 4. Challenges Faced & Solutions

Model Endpoint Failures: Standard LLM client configurations failed during initial model initialization; resolved by explicitly passing provider configurations and fallback flags for OpenRouter execution.

Git History Secret Leakage: Accidental .env commits locked history state and triggered GitHub Secret Scanning blocks; resolved by resetting the Git tree inside an isolated project directory.

Classification Ambiguity: Overlapping intent between generic work emails and urgent requests was eliminated by refining field descriptions in the Pydantic schema to improve context evaluation.

🛠️ Tech Stack

Python (3.10+)

LangChain & LangGraph (Agentic Workflow Orchestration)

OpenRouter API (qwen/qwen-2.5-72b-instruct)

Pydantic (Data Validation & Structured Schemas)

Python-Dotenv (Environment Management)
