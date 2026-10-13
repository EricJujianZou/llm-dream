"""
LongMemEval judge, two labels on every answer (decisions.md, "Main judge", 4 Oct 2026).
Prompt templates are taken verbatim from external/longmemeval_evaluate_qa.py (xiaowu0162/LongMemEval, MIT).
Main judge: gpt-5.6-luna on the OpenAI key, label = 'yes' in the reply, as in LongMemEval's own evaluation code.
Second judge: claude-opus-5-5 through the pinned wrapper, answer constrained to yes or no by a JSON schema.
"""
import ast, json, os, pathlib
import api

ROOT = pathlib.Path(__file__).resolve().parent.parent
_src = (ROOT / "external" / "longmemeval_evaluate_qa.py").read_text()
_tree = ast.parse(_src)
_fn = next(n for n in _tree.body if isinstance(n, ast.FunctionDef) and n.name == "get_anscheck_prompt")
_ns = {}
exec(compile(ast.Module(body=[_fn], type_ignores=[]), "longmemeval_prompt", "exec"), _ns)
get_anscheck_prompt = _ns["get_anscheck_prompt"]

MAIN_JUDGE = os.environ.get("WP_MAIN_JUDGE", "gpt-5.6-luna")
SCHEMA = {"type": "object", "properties": {"answer": {"type": "string", "enum": ["yes", "no"]}},
          "required": ["answer"], "additionalProperties": False}
JUDGE_SYSTEM = "You are grading a model's answer. Follow the instructions in the message exactly and reply with yes or no."


def judge_opus(prompt, tag):
    try:
        r = api.call(JUDGE_SYSTEM, [{"role": "user", "content": prompt}], tag=f"{tag}/judge_opus", max_tokens=2000,
                     cache_system=False, json_schema=SCHEMA)
    except api.Refusal:
        return False, "judge_refusal"
    try:
        label = json.loads(r["text"])["answer"]
    except Exception:
        label = r["text"].strip().lower()[:10]
    return label.startswith("yes"), label


def judge_openai(prompt, tag, model=MAIN_JUDGE):
    text, _ = api.openai_chat(model, prompt, tag=f"{tag}/judge_{model}", max_completion_tokens=2000)
    return "yes" in text.lower(), text[:40]


def judge(question_type, question, answer, response, abstention, tag):
    """Returns {correct, judge_label, correct_opus, judge_label_opus, judge_main}. `correct` is the main judge."""
    prompt = get_anscheck_prompt(question_type, question, answer, response, abstention=abstention)
    c_main, l_main = judge_openai(prompt, tag)
    c_opus, l_opus = judge_opus(prompt, tag)
    return {"correct": c_main, "judge_label": l_main, "correct_opus": c_opus, "judge_label_opus": l_opus, "judge_main": MAIN_JUDGE}
