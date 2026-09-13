"""Checks that bundle splitting stays conservative.

The failure that matters here is not "missed a subject" -- that just leaves a
bundle unresolved, which is a supported outcome. It is "invented a subject",
which hands a student the wrong paper while looking authoritative. Most of
these cases therefore assert that the splitter REFUSES.

Usage:
    .venv/bin/python -m tests.test_pyq_pdf_subjects
"""
import normalization.pyq_pdf_subjects as pdf_subjects
from normalization.pyq_normalizer import build_alias_index, load_subjects

HEADER = "K J Somaiya College of Engineering\nEnd Semester Examination\n"

# (label, pages, expected subject_keys in order)
CASES = [
    ("clean three-subject bundle, continuation pages inherit",
     [HEADER + "Subject: Operating Systems\nQ1 explain paging",
      "Q2 more paging text",
      HEADER + "Subject: Database Management System\nQ1 normalize",
      "Q2 sql joins",
      HEADER + "Subject: Computer Networks\nQ1 tcp"],
     ["os", "dbms", "cn"]),

    ("only one subject -- not a bundle, refuse to split",
     [HEADER + "Subject: Operating Systems\nQ1", "Q2", "Q3"],
     []),

    ("scanned or unreadable PDF -- refuse",
     [],
     []),

    ("header naming two subjects is ambiguous -- refuse",
     [HEADER + "Operating Systems and Computer Networks combined\nQ1",
      HEADER + "Subject: Machine Learning\nQ1", "more ml"],
     []),

    ("too few pages resolved to trust the split -- refuse",
     [HEADER + "Subject: Operating Systems"] + ["filler " * 40] * 12,
     []),

    ("a subject mentioned deep in a question body is not that page's subject",
     [HEADER + "Subject: Operating Systems\nQ1 paging",
      "Q2 " + "pad " * 300 + " compare this with database management system ",
      HEADER + "Subject: Computer Networks\nQ1 tcp"],
     ["os", "cn"]),
]


def main():
    alias_index = build_alias_index(load_subjects())
    subjects = load_subjects()
    failures = []
    real_page_texts = pdf_subjects.page_texts

    for label, pages, expected in CASES:
        pdf_subjects.page_texts = lambda _b, max_pages=400, _p=pages: _p
        try:
            spans = pdf_subjects.extract_subject_pages(b"stub", alias_index,
                                                       subjects)
        finally:
            pdf_subjects.page_texts = real_page_texts
        got = [s["subject_key"] for s in spans]
        if got != expected:
            failures.append(f"{label}: got {got}, expected {expected}")
        # Page ranges must be 1-based, ordered and non-overlapping.
        for a, b in zip(spans, spans[1:]):
            if a["page_end"] >= b["page_start"]:
                failures.append(f"{label}: spans overlap {a} / {b}")
        for span in spans:
            if span["page_start"] < 1 or span["page_end"] < span["page_start"]:
                failures.append(f"{label}: bad page range {span}")

    if failures:
        print(f"FAILED: {len(failures)} check(s)")
        for f in failures:
            print("  -", f)
        return 1
    print(f"All PDF bundle-splitting checks passed ({len(CASES)} cases).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
