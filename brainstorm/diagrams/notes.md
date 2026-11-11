# Diagram notes

Brainstorm for the owner, 2026-11-10. Nothing in `docs/diagrams/` or in the office180 repository was touched.

## Files here

| File | What it is | validate / resolve / text-fit | Compiles to PPTX |
|---|---|---|---|
| `chain-v2a.vector180.svg` (+ `.png`) | Layout A: three lanes by kind (checks, artefacts, tools), same left-to-right order as today | pass / pass / 38 clear, peak 90% | yes, 146 native objects |
| `chain-v2b.vector180.svg` (+ `.png`) | Layout B: three zones by layer (Requirement, Code, Lean); the two sides descend and meet at the proof | pass / pass / 34 clear | yes, 129 native objects |
| `shapes-demo.vector180.svg` (+ `.png`) | Top row: what lines, rects and circles alone can draw. Bottom row: the same with asset groups | pass / pass / 22 clear | no, on purpose (assets and an `rx` rect); the top row alone compiles |
| `vector180-proposal.md` | Measured capability table and a proposal for native arrowheads, diamonds and rounded boxes | | |

The PNGs are Quick Look thumbnails cropped to the viewBox. Quick Look has no ABeeZee, so they show a serif fallback, close to what GitHub shows. The compiled PPTX of both layouts was thumbnailed with Quick Look and matched the SVG; it was not opened in PowerPoint.

The atoms come from a small Python generator in session scratch (`/private/tmp/claude-501/-Users-will-dev-lean-rosette/d7525621-3840-4005-8780-0588ba995cd8/scratchpad/diagrams-agent-work/gen.py`), which will not survive. With 130 to 150 objects per figure the generator, not the SVG, is the real source. If either layout is adopted, the generator should be saved in the repository; I did not, because the brief limited which files I may write.

## 1. Arrows and diamonds: yes, and natively

Both are possible in Vector180 0.1 with no asset group. The full measured table is in `vector180-proposal.md`.

| Want | Native construction | Cost |
|---|---|---|
| Arrowhead | Two short `line`s meeting at the tip (open chevron), grouped with the shaft | Three objects per arrow; in PowerPoint the head is separate strokes |
| Right-angle route | One `line` per segment, each overlapping the corner by half a stroke | One more object per bend |
| Diamond, hexagon | Four or six `line`s | Outline only, no fill; a hairline notch at each vertex when zoomed in |
| Pill | A stroke-less `rect` plus two stroke-less `circle`s in one fill | Filled only, no outline |
| Filled diamond, outlined rounded box, curves, dashes, solid arrowheads | Asset group (any SVG inside), or `rx` on a rect | **`compile` refuses the whole atom** if it contains one asset or one `rx` rect |

Two traps found on the way: `validate` passes several things `resolve` rejects (markers, dashes, `polyline`), so always run both; and `compile` rejects geometry that is not a whole or half unit.

Both new layouts are fully native. That decided the shape vocabulary: checks are outline diamonds, tools are filled pills with no outline, artefacts are square outlined boxes. Three kinds, told apart by shape alone, without colour.

## 2. The "states on top, transformers below" suggestion

Half right.

**Right:** the current figure mixes kinds. Its bottom row blends activities ("composition"), questions and evidence, and its top-row boxes are coloured by the neighbouring link, so colour means nothing in particular. Naming a link for the thing that does it (the compiler, not "compilation") is a clear gain.

**Wrong if followed literally, in three ways:**

1. **Not every link makes something.** The author confirming the echo and the kernel checking a proof compare two artefacts and produce a judgement. Calling them transformers hides the distinction the project is about: generated versus checked.
2. **It is not a pipeline.** People write two things, the English rule and the Rust source, at opposite ends. The sentence compiler runs left to right, the translator right to left, the Rust compiler left to right again, away from the middle. A row of right-pointing arrows would be false.
3. **One check does not sit between neighbours.** The test that backs the translation runs the same inputs on the Lean model and on the *compiled* Rust. It skips over Rust source, so it is partial evidence for translation and compilation together. The current figure and the architecture table file it under translation only.

So both layouts have three kinds, and colour has one job:

- **Box = artefact.** No colour: an artefact is not evidence.
- **Pill + arrow = tool that makes the next artefact**, with the arrow pointing the way it really runs. Under it, in words, how far it is trusted: "output is checked", "trusted tool", "trusted".
- **Diamond = check.** Joined by plain lines, no arrowheads, to the two artefacts it compares. It names who judges and carries the evidence kind in words.
- **Colour = what the link rests on:** amber a person's judgement, green a machine check, blue tested, grey trust alone.

A consequence I think is correct: today's single tag "tool-trusted, tested" for translation splits into a trusted tool (the pill) and a tested relation (the blue diamond). The architecture document says never to blend an assumption with a piece of evidence; the current tag does.

Following the Reach figure the coordinator pointed to, the boxes hold one or two words and nothing else; the questions and explanations from the current figure belong in the README text and in the architecture table, which already has them.

## 3. Which layout

**Recommend B.** Use A in ARCHITECTURE section 2 only if two figures are wanted.

Layout B

- Its shape is the argument: requirement on the left, code on the right, both brought down into Lean, and the proof is the largest object, joining them.
- Directions need no explaining: two arrows leave Rust source, one down into Lean, one sideways to the compiler.
- The test check visibly sits outside the Lean zone, tying the model to the running code.
- "Reading" is shown as what it is to a person: something the compiler hands back, which the author compares with the rule.
- Weaknesses: it drops the composition link (reading to Lean statement, machine-checked), so it shows four links where the architecture table has five. The README's sample report also prints four, so this is consistent with the README and not with ARCHITECTURE. The cross-check diamond floating outside every zone looks slightly orphaned. The top-right corner of the Requirement zone is empty.

Layout A

- Keeps the order the report prints under "Rests on", so each column lines up with a row of the architecture table, and it keeps all five links.
- One sentence compiler visibly feeds both the reading and the statement.
- The empty slot above the Rust compiler ("compiler: no check") makes the missing check visible, which is the honest thing about that link.
- Weaknesses: at first glance it still reads as a pipeline, the impression to get rid of. The long blue line over Rust source can be misread as attached to it. Three diamonds in a row with near-identical brackets make the kernel check look no more important than the type-check.

Unsure, and to be checked against `slice/` before either ships:

- Whether "reading" and "Lean statement" are two outputs of the compiler (as B draws) or one feeds the other (as A draws). ARCHITECTURE says the compiler writes the Lean term and a separate link step proves the reading equivalent to the statement that was proved. If so, the green diamond in A should say "proved equivalent", which is stronger than "type-checks", and B should gain a small check between Reading and Lean statement.
- The proof text is an artefact too (written by a person or an agent, not trusted). Neither layout shows it. Adding it to B as an input to the kernel diamond is cheap and makes a point the README makes in words.
- "Author confirms" stands for two human acts: the once-per-piece vocabulary sign-off and the once-per-sentence echo confirmation. The reuse story lives in that difference. It belongs in the vocabulary figure; the two figures should use the same amber for it.
- The title "Two things people write are brought into Lean, where the proof is" is mine. The README heading may make any title unnecessary.

Readability at README width: the canvas is 1600 and GitHub shows about 850, so the 23-unit box labels land near 12 px and the 17-unit tags near 9 px. The labels are fine; the tags and legend are at the limit. If they prove too small, redraw on a 1200 canvas with the same word count; do not add words.

## 4. The other three figures

Give all four one vocabulary and one legend strip, identical in each: box = artefact, pill = tool, diamond = check, colour = what it rests on.

Today colour changes meaning from figure to figure. Blue is "domain word" in vocabulary, "translation" in the chain, "translator" in pipeline and "property tests" in evidence. Purple is "modifier", then "search and tests", then "bounded check". Amber is "reading", "vocabulary", "sentence compiler" and "a compiled rule". A reader who learns the code in one figure is misled by the next. All three also carry two or three lines of body text per box at 17 to 19 units, which is about 9 px on GitHub.

**vocabulary** (the best of the four; keep the structure)

- Piece kinds are not evidence, so take them off the evidence palette: three neutral tints, or one hue family used nowhere else. Keep amber for the one human-asserted thing here, the sign-off: a small amber "signed once" tag on each library says more than colouring the box.
- The dots under the libraries should be arrows into the compiled reading.
- Show reuse, which is the point and is only in the subtitle today: a second, greyed sentence built from the same pieces with "0 new pieces" beside it.
- Cut the body text in the three library boxes to the example words only.

**pipeline** (the weakest; it has exactly the fault the owner named)

- Its middle column lists two tools (sentence compiler, translator), two checks (kernel, audit) and one mixture (search and tests) as five identical rectangles in five colours. Make them pills and diamonds.
- Its connectors join columns at arbitrary boxes, which reads as a relation that does not exist. Draw real edges or none.
- Once the chain figure shows tools and checks, this one mostly repeats it. I would cut it to "what you write, what you get back" in two columns, or drop it: the step table under it in ARCHITECTURE does the job better.

**evidence**

- Its tags (tested, sampled, bounded, kernel-checked) and the chain's (human-asserted, machine-checked, kernel-checked, tested, trusted) are two word lists for one idea. Settle one list. Suggestion: green for kernel-checked, one blue family for everything finite (examples, samples, bounded), with the bound in words.
- The line under the cards implies one scale from weak to strong, which ARCHITECTURE explicitly rejects. Label it as cost and coverage, and give it an arrowhead.
- "A compiled rule" is amber, which elsewhere means a person's judgement. It is a generated artefact: plain box.
- Each tier is a check, so each could be a diamond. Four diamonds in a row may be too much. Unsure; try it.

## 5. Should the hero image be this figure?

No. Neither layout, and not the current chain. A hero gets two seconds at 850 px or less; these are the second picture, for someone who has already decided to read.

In order of preference:

1. **No hero image.** The README already opens with the Gherkin rule and the report block, which GitHub renders crisply, in the reader's theme, at a readable size. A picture repeating them less legibly is a loss.
2. **A three-object cut of layout B:** "English rule", "Rust source", and one green diamond between them, "proved for every input". No tools, no zones, no legend, type twice the size. Cheap to make from the same generator, and it would sit well directly under the tagline.
3. **Before and after as a picture of the product:** the rule on the left, the verdict with its four "Rests on" lines and colour chips on the right. It introduces the colours every later figure uses, but it needs about twelve lines of text, which is a lot for a hero.

A caution that applies to 2 and 3: "Where it stands" says a new sentence cannot yet run end to end without hand-written glue. A hero makes the target look like the present more strongly than text does. If one is added, the caption should say it is the target.

I did not review the awesome-readme list; `brainstorm/readme-patterns.md` covers it, and its "one diagram above the second heading" advice is compatible with option 2.

## What happened to an earlier draft

When I came to write these files, `notes.md` and `vector180-proposal.md` already existed in this folder, written a few minutes earlier by what appears to be a parallel run of this same task (same experiments, same scratch folder). Its two chain layouts used body text inside the boxes and, in one, asset shapes; they predated the instruction to follow the Reach figure. My copies of the three atoms and PNGs replaced its files of the same names before I noticed, and my scratch cleanup removed its preview PNGs. Its atoms are not recoverable from here. I kept its proposal and amended it, and rewrote these notes to describe the atoms now in the folder. Its compiled PPTX remains at `/private/tmp/claude-501/-Users-will-dev-lean-rosette/d7525621-3840-4005-8780-0588ba995cd8/scratchpad/pptx/chain-v2b.pptx` if that layout is wanted for comparison.
