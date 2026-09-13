"""Minimal FastAPI app for the KJGPT prototype.

Run with:
    uvicorn main:app --reload

Endpoints:
    POST /ask        -> {"question": "..."}                  -> {"answer": "..."}
    POST /ask/debug   -> {"question": "..."}                  -> full trace (dev only)
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from services.faculty_service import answer_faculty_question
from services.policy_service import answer_policy_question, answer_policy_question_llm
from services.pyq_service import answer_pyq_question

app = FastAPI(title="KJGPT Prototype")


class Question(BaseModel):
    question: str


class PolicyQuestion(BaseModel):
    question: str
    # Off by default. The corpus holds a 2018 handbook edition whose
    # examination rules were replaced when the institute became autonomous;
    # answering a current student from it would be worse than saying nothing.
    include_superseded: bool = False
    # Off by default, same contract as PYQQuestion.use_llm: the deterministic
    # path stays the default so existing callers/tests are unchanged. When
    # true, Qwen synthesizes the final answer from the same retrieved
    # provisions under the Policy-domain system prompt stored on the graph.
    use_llm: bool = False


class PYQQuestion(BaseModel):
    question: str
    # Off by default: the answer is a list of links retrieval already found,
    # so the model can only slow it down (~15s vs ~2ms) and occasionally drop
    # a row. Turn it on when conversational phrasing matters more than speed.
    use_llm: bool = False


@app.post("/ask")
def ask(payload: Question):
    try:
        result = answer_faculty_question(payload.question, debug=False)
        return result
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))


@app.post("/ask/debug")
def ask_debug(payload: Question):
    """Development-only endpoint. Returns the full retrieval + LLM trace."""
    try:
        return answer_faculty_question(payload.question, debug=True)
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))


@app.post("/pyq/ask")
def pyq_ask(payload: PYQQuestion):
    """Previous-year question papers -> Google Drive links.

    Returns {"answer": str, "papers": [{title, drive_url, ...}]}. The papers
    list is the machine-readable form; a UI should link those directly rather
    than parsing URLs back out of the answer text.
    """
    try:
        return answer_pyq_question(payload.question, debug=False,
                                   use_llm=payload.use_llm)
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))


@app.post("/pyq/ask/debug")
def pyq_ask_debug(payload: PYQQuestion):
    """Development-only. Shows the extracted filters and the context built."""
    try:
        return answer_pyq_question(payload.question, debug=True,
                                   use_llm=payload.use_llm)
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))


@app.post("/policy/ask")
def policy_ask(payload: PolicyQuestion):
    """Institute Policy Handbook questions -> sourced provisions.

    Returns {"answer": str, "sources": [{policy, document, page, section, url,
    status}], "found": bool}. Every fact in `answer` is traceable to a page of
    a named PDF via `sources`. When `found` is false the answer says so rather
    than offering the nearest thing it could find.
    """
    try:
        fn = answer_policy_question_llm if payload.use_llm else answer_policy_question
        return fn(payload.question, include_superseded=payload.include_superseded)
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))


@app.post("/policy/ask/debug")
def policy_ask_debug(payload: PolicyQuestion):
    """Development-only. Adds the fulltext query and the provisions retrieved."""
    try:
        fn = answer_policy_question_llm if payload.use_llm else answer_policy_question
        return fn(payload.question, debug=True,
                  include_superseded=payload.include_superseded)
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
