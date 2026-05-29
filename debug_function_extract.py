def format_response(response: str, style: str) -> str:
    if not isinstance(response, str):
        return response

    text = _normalize_text(response)
    sentences = []
    for part in re.split(r"\n+", text):
        sentences.extend(_split_sentences(part))
    sentences = [s.strip() for s in sentences if s.strip()]

    if not sentences:
        return (
            "MAIN IDEA\n"
            "No answer content was returned.\n\n"
            "EXPLANATION\n"
            "The system did not provide usable text for formatting.\n\n"
            "KEY POINTS\n"
            "- Empty response\n"
            "→ Meaning: there was no answer to convert into a structured explanation.\n\n"
            "FINAL SUMMARY\n"
            "No structured teaching output could be formed.\n\n"
            "RELATED DOUBTS\n"
            "- What input will produce a usable answer?\n"
            "- Is the AI response service working correctly?"
        )

    def _truncate(line: str, max_length: int = 140) -> str:
        if len(line) <= max_length:
            return line
        return line[: max_length - 3].rsplit(" ", 1)[0] + "..."

    def _meaning_for(point: str, sentence: str) -> str:
        cleaned = point.rstrip(".")
        if "=" in cleaned:
            left, right = cleaned.split("=", 1)
            return (
                "It expresses how "
                + left.strip()
                + " depends on "
                + right.strip()
                + "."
            )
        if " is " in cleaned:
            left, right = cleaned.split(" is ", 1)
            return (
                "That identifies "
                + right.strip()
                + " as the value for "
                + left.strip()
                + "."
            )
        if " are " in cleaned:
            left, right = cleaned.split(" are ", 1)
            return (
                "It shows that "
                + left.strip()
                + " are described by "
                + right.strip()
                + "."
            )
        words = cleaned.split()
        if len(words) <= 6:
            return "It explains that " + cleaned + " in a clearer way."
        return (
            "It explains that "
            + " ".join(words[: min(10, len(words))])
            + ("..." if len(words) > 10 else "")
            + "."
        )

    def _fresh_summary(main_line: str, point: str) -> str:
        alpha = point.rstrip(".")
        if "=" in alpha:
            return "Overall, the formula links the key variables into a single explanatory relationship."
        return "Overall, the main idea is framed so the topic can be understood by focusing on " + alpha.lower() + "."

    max_explanation = 3
    max_points = 3
    if style == "medium":
        max_explanation = 4
        max_points = 4
    elif style == "detailed":
        max_explanation = 5
        max_points = 5
    elif style == "long":
        max_explanation = 6
        max_points = 5
    elif style == "direct":
        max_explanation = 3
        max_points = 2
    elif style == "short":
        max_explanation = 3
        max_points = 3

    used = set()

    main_idea_lines = []
    first_line = _truncate(sentences[0], 140)
    main_idea_lines.append(first_line)
    used.add(first_line)
    if len(sentences) > 1:
        second_candidate = sentences[1]
        if second_candidate not in used and second_candidate.lower() not in first_line.lower():
            main_idea_lines.append(_truncate(second_candidate, 140))
            used.add(second_candidate)

    explanation_lines = []
    for sentence in sentences[1:]:
        if len(explanation_lines) >= max_explanation:
            break
        if sentence in used:
            continue
        explanation_lines.append(_truncate(sentence, 160))
        used.add(sentence)
    if len(explanation_lines) < 3 and len(sentences) > len(explanation_lines) + 1:
        extra = sentences[len(explanation_lines) + 1 :]
        for sentence in extra:
            if len(explanation_lines) >= 3:
                break
            if sentence in used:
                continue
            fragments = re.split(r",\s+|;\s+| -\s+", sentence)
            for fragment in fragments:
                fragment = fragment.strip()
                if fragment and fragment not in used:
                    explanation_lines.append(_truncate(fragment, 160))
                    used.add(fragment)
                if len(explanation_lines) >= 3:
                    break
    explanation_lines = _ensure_lines(explanation_lines, min(3, max_explanation))

    key_points = []
    remaining_sentences = [s for s in sentences if s not in used]
    for sentence in remaining_sentences:
        if len(key_points) >= max_points:
            break
        point = sentence.split(",")[0].strip()
        if not point or len(point.split()) < 3:
            continue
        point = _truncate(point, 90)
        if any(point.lower() == kp[0].lower() for kp in key_points):
            continue
        meaning = _meaning_for(point, sentence)
        if meaning.lower().startswith(point.lower()):
            meaning = "That idea describes " + point.lower() + " with a different phrase."
        if meaning in used:
            meaning = "That idea is highlighted here with new wording."
        key_points.append((point, meaning))
        used.add(point)
        used.add(meaning)
        used.add(sentence)

    if not key_points:
        for sentence in explanation_lines[:3]:
            point = sentence.split(",")[0].strip()
            if not point or point in used:
                continue
            meaning = _meaning_for(point, sentence)
            key_points.append((point, meaning))
            used.add(point)
            used.add(meaning)
            if len(key_points) >= 2:
                break

    formula = None
    formula_explanation = None
    formula_match = re.search(r"\b[a-zA-Z][a-zA-Z0-9_]*\s*=\s*[^,;\n]+", text)
    if formula_match:
        candidate = formula_match.group(0).strip()
        if candidate not in used:
            formula = candidate
            formula_explanation = "→ Meaning: This formula describes the complete relation between the left side and the right side." 
            used.add(formula)
            used.add(formula_explanation)

    cases = []
    case_keywords = ["example", "if ", "when ", "in case", "otherwise", "instead", "case ", "scenario"]
    for sentence in sentences:
        low = sentence.lower()
        if any(keyword in low for keyword in case_keywords) and sentence not in used:
            case_phrase = sentence.split(".")[0].strip()
            if not case_phrase:
                continue
            meaning = "→ Meaning: " + _truncate(case_phrase, 120)
            if meaning in used:
                meaning = meaning + " with added clarity."
            cases.append((case_phrase, meaning))
            used.add(case_phrase)
            used.add(meaning)
        if len(cases) >= 3:
            break

    if key_points:
        summary_point = key_points[0][0]
    elif explanation_lines:
        summary_point = explanation_lines[0]
    else:
        summary_point = main_idea_lines[0]
    final_summary = _fresh_summary(main_idea_lines[0], summary_point)
    if final_summary in used:
        final_summary = "In summary, the core idea is organized as a teaching note for clear understanding."

    related_doubts = []
    if formula:
        left_side = formula.split("=", 1)[0].strip()
        related_doubts.append(f"What happens if {left_side} changes in this formula?")
        related_doubts.append("Can this formula still apply when the inputs shift?")
        if key_points:
            related_doubts.append(
                "How does the topic change when " + key_points[0][0].lower() + " varies?"
            )
    elif cases:
        related_doubts.append(
            "What happens if " + cases[0][0].lower() + " changes?"
        )
        related_doubts.append("Is this behavior consistent in every related case?")
        if len(cases) > 1:
            related_doubts.append(
                "How does the outcome differ when another case is present?"
            )
    else:
        topic_phrase = main_idea_lines[0].split(".")[0].strip()
        if len(topic_phrase.split()) > 8:
            topic_phrase = " ".join(topic_phrase.split()[:8])
        related_doubts.append(
            "What happens if " + topic_phrase.lower() + " is used in a different context?"
        )
        related_doubts.append(
            "Is the main idea always valid under varying conditions?"
        )
        if key_points:
            related_doubts.append(
                "How does the answer change when " + key_points[0][0].lower() + " is altered?"
            )

    related_doubts = [q for i, q in enumerate(related_doubts) if q not in related_doubts[:i]]
    related_doubts = related_doubts[:3]

    out = ["MAIN IDEA"]
    out.extend(main_idea_lines[:2])
    out.append("")

    out.append("EXPLANATION")
    out.extend(explanation_lines[:max_explanation])
    out.append("")

    if key_points:
        out.append("KEY POINTS")
        for point, meaning in key_points:
            out.append(f"- {point}")
            out.append(f"→ Meaning: {meaning[len('It explains that '):] if meaning.startswith('It explains that ') else meaning}")
        out.append("")

    if formula:
        out.append("FORMULA")
        out.append(formula)
        out.append(formula_explanation)
        out.append("")

    if cases:
        out.append("BEHAVIOR / CASES")
        for case_text, case_meaning in cases:
            out.append(f"- {case_text}")
            out.append(case_meaning)
        out.append("")

    out.append("FINAL SUMMARY")
    out.append(final_summary)
    out.append("")

    out.append("RELATED DOUBTS")
    for question in related_doubts:
        out.append(f"- {question}")

    cleaned = []
    seen_lines = set()
    for line in out:
        line = line.strip()
        if not line:
            if cleaned and cleaned[-1] != "":
                cleaned.append("")
            continue
        if line in seen_lines:
            continue
        cleaned.append(line)
        seen_lines.add(line)

    return "\n\n".join(cleaned).strip()

