# Intelligent questions: minimum information, maximum design freedom

## First pass

Inspect the input without questioning the user about things visible in the image. Infer the subject type, number of salient subjects, approximate orientation, source-background complexity, content safety and potential text-safe regions. Inferred intent is a hypothesis, not a hard fact.

Before creating, gather enough to avoid consequential errors:

1. **Purpose / audience / occasion** — if ambiguous and affects creative direction.
2. **Exact required content** — headline, dates, venue, names, price, CTA, brand and legal wording. Never fabricate details.
3. **Canvas** — ratio, physical dimensions/platform if unknown and consequential.

At most **three focused questions in one turn**. Prefer one combined, natural question when only one detail matters. Do not use a bulky questionnaire. If the user says "you decide", set safe defaults and explain them briefly.

## Defaults (overridable)

- Social poster with no size specified: propose portrait `4:5`, 1080×1350; if user's original image is landscape and important content would be lost, use `16:9` or ask.
- Unknown mood: infer from the source and goal, mark it as suggested, not supplied.
- Unknown title: offer a clearly marked draft line, do not present invented factual claims as user-approved copy.
- No CTA: omit it unless the purpose explicitly calls for conversion.
- Source image should preserve distinctive people, pets, products and logos; seek confirmation only if replacing them is central to the concept.
- If user asks to copy a reference precisely, explain the originality boundary; offer a fresh composition using transferable principles.

## Example

Source: crowded photo with two people; user says "做张生日海报".

Ask: "海报写给谁？必须出现的祝福语是什么？你希望发朋友圈竖版（默认 4:5），还是另有尺寸？"

If user replies "给奶奶，祝奶奶生日快乐，其他随意": stop asking. Use exact blessing, select mood based on photo, keep both people recognizable, avoid cropping faces.

## Confirmations and friction

- Warn before irreversible cropping, brand distortion, unverified claims or public-library writes.
- Don't ask for favorite font, palette, 12 keywords, style taxonomy or resolution unless needed.
- Keep open-ended questions actionable; support "自动决定" as a valid answer.
- Ask for missing image only when none was provided and it is essential to the visual task.
