# Contributing to Poster Genome

Help make reusable visual knowledge more specific, honest and useful.

## Welcome contributions

- Original genomes with explicit design reasons, adaptation rules and failure modes
- Better analysis of composition, type, color and subject treatment
- Chinese typography and layout guidance
- Tests, opt-in image-generation integrations and visual review methods

## Add a genome

1. Compare with existing genomes to avoid near duplicates.
2. After the user's approval, scaffold a draft:

   ```bash
   python scripts/new_genome.py --id new-design-dna --title "My style" --summary "What makes this useful"
   ```

3. Replace every `REPLACE` placeholder, document what source images suit it, record provenance and set `active` only after review.
4. Run the JSON Schema validation and unit tests; add a matching case if the style differs meaningfully.
5. Explain the compositional *reason* and an example of where the genome fails.

## Rights and privacy

Do not commit unlicensed third-party posters, source photos, brand assets, paid fonts, watermarked images, identifiable personal photos, private briefs or credentials. Only contribute content you can license under MIT or explicitly clarify exceptions without committing restricted files.

## Pull request checklist

- [ ] File name equals `id` and semantic version is intentional
- [ ] Source, rights and certainty are recorded honestly
- [ ] Three or more actionable rules and a meaningful failure mode
- [ ] Both scripts and tests pass locally
- [ ] No extra private photos or fonts
