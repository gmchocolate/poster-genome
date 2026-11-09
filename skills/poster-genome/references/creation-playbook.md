# Art direction and poster production

## 1. Build the production brief

Separate non-negotiable constraints (exact headline, names, numbers, logo, safety, recognizability, aspect ratio) from adjustable taste (mood, palette, atmosphere). Determine whether the input is a background, focal subject, full scene or logo. Identify potential crops, occlusion and text-safe regions. If resolution is weak, note the limitation and prefer simpler treatments.

## 2. Compose before rendering

Write a short **visual blueprint** that specifies:

- **One sentence concept**: what it should feel like and communicate.
- **Canvas**: aspect, pixels/medium, intended viewing distance, padding/safe area.
- **Hierarchy**: first glance, second glance, action/details.
- **Subject**: exact source item to retain; focal position, scale, crops, light/depth.
- **Text boxes**: top/left/width/height estimates; line breaks, relative type scale, alignment and maximum lines.
- **Layers**: background → environmental treatment → subject → accents → typography → marks/CTA.
- **Palette**: base, text and highlight roles, with adequate contrast; don't overuse accents.
- **Adaptations**: what changes if the headline is twice as long, subject is off-center or aspect changes.

Use the selected genome's grammar, not its literal sample composition. Add only visual elements with a communicative purpose.

## 3. Image generation or editing

Prefer actual image editing for user-provided photos when the host can preserve identity; ask for a source crop or mask only when it materially improves the result. If using generation, direct the model to preserve relevant identity, avoid invented text/logo and leave required text zones clear. Distinguish a *visual draft* from a final export.

Suggested rendering instructions (adapt to the actual tool):

> Create an original poster artwork. Canvas [ratio]; main subject [source identity and preserve instructions]; composition [specific blueprint]; palette [roles]; lighting [effects]; texture [restrained treatment]; preserve space for exact typography in [zones]. Do not introduce random letters, watermarks, unrequested logos or extra faces. Avoid copying any single reference poster's distinctive full composition.

If exact copy is essential and the image tool produces garbled letters, perform text placement with a reliable editable typography layer rather than accepting misspellings. Do not invent typography tools or claim fonts installed.

## 4. Copywriting

- Ask for text that must be exact; never invent venue, date, pricing, endorsements or guarantees.
- Suggest alternatives only where the user delegated copywriting.
- Structure headline first, then one explanatory subtitle, then details/CTA if relevant.
- Prefer clear, human-readable wording over pseudo-luxury jargon and generic AI marketing clichés.
- For Chinese: make line breaks natural; avoid isolated single characters at line ends or awkward splitting of names.

## 5. Export and technical checks

Check real output dimensions, ratio, clipping, image subject fidelity, important margin, line readability at target size, color consistency and all visible characters. For print, request actual bleed/trim/profile requirements and use appropriate tools; do not claim a screen PNG is CMYK-ready print art. For social, export at actual platform size where possible.

If no renderer exists, deliver a clear blueprint with edit-ready copy, positional descriptions and prompts that another designer/tool can execute, explicitly saying no image was generated.
