# Poster quality review — gate, score, iterate

Review the *visible actual output*, not only its prompt. When no image is available, review the plan and mark visual quality **unverified**.

## Gate 0: hard failures (fix before delivery)

- Exact supplied characters/digits, names, logos or claims are wrong, invented or missing.
- Main face, product, pet or required object is distorted, swapped, hidden or cropped contrary to brief.
- Wrong format/size, broken export, unreadable key text, illegible text over texture or text clipped by the canvas.
- Unapproved source cloning, unlicensed redistributed visual material, watermark removal, misleading factual material.

## Weighted design rubric (0–5 each)

| Dimension | Weight | Ask |
| --- | ---: | --- |
| Message and first-glance clarity | 20 | Do viewers know what it is about immediately? |
| Visual hierarchy and layout | 20 | Is there a clear reading path, focus and rhythm? |
| Typography and actual legibility | 20 | Are lines, spacing, balance, type roles and exact content coherent? |
| Subject integrity and imagery | 15 | Is source recognizability preserved? Does cropping/light work? |
| Palette, atmosphere and restraint | 15 | Do contrast and texture reinforce intent without noise? |
| Technical delivery | 10 | Are edges, size, safe margins and exports usable? |

Calculate weighted score as `sum((rating / 5) * weight)`, max 100. **These numbers are subjective review aids, not universal aesthetic truths.** Explain scores with specific evidence, not generic praise.

## Iteration discipline

1. List top 1–3 issues with visible evidence and severity.
2. Separate blocking defects from style preferences.
3. State a precise change instruction: what to adjust, what must remain unchanged, how success will look.
4. Regenerate/edit the affected visual layers if possible; reassess. Limit gratuitous full-scene regeneration that sacrifices identity and copy.
5. Deliver only after hard-failure gates are passed. If not fixable with the host tools, name the remaining defect without claiming the work is publish-ready.

## Quick thumbnail review

Would it be understandable and distinctive when shown on a small phone screen? If not, simplify competing accents, improve headline contrast or enlarge the hero instead of adding more elements.
