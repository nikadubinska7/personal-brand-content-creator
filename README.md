# Personal Brand Content Creator

Local MVP for generating personal-brand LinkedIn content from markdown knowledge
base files.

## Knowledge Base Check

Run the document processing foundation from the project root:

```bash
python src/main.py
```

The command loads markdown files from:

- `knowledge_base/primary/`
- `knowledge_base/secondary/`

It prints the number of files loaded, the file names, and a short preview of the
combined context. It also builds a reusable idea-generation prompt preview from
the markdown context. This step does not call the OpenAI API.

## Generate Ideas

To generate 5 LinkedIn post ideas, add `OPENAI_API_KEY` to `.env` and run:

```bash
python src/main.py --generate-ideas
```

You can optionally set `LLM_MODEL` in `.env`. If not set, the app uses
`gpt-4o-mini`.

## Build A Content Prompt

After selecting an idea, preview a format-specific prompt without calling the
API:

```bash
python src/main.py --format text --idea "AI can reduce manual follow-up work in supplier communication"
```

Supported formats are `text`, `carousel`, and `listicle`.

To generate the selected content with OpenAI, add `--generate-content`:

```bash
python src/main.py --format carousel --idea "AI can support logistics exception management" --generate-content
```

Add `--save-output` to save generated ideas or generated content as markdown in
`outputs/`:

```bash
python src/main.py --generate-ideas --save-output
```

For carousel or listicle content, add `--save-pdf` to export a readable PDF:

```bash
python src/main.py --format listicle --idea "AI can support weekly reporting" --generate-content --save-output --save-pdf
```

## Uniqueness Evidence

Preview a comparison prompt by providing a generic baseline and app output:

```bash
python src/main.py --generic-output "Generic AI post text" --app-output "Knowledge-base app post text"
```

Add `--generate-uniqueness` to call OpenAI and create comparison evidence for
project documentation. Add `--save-output` to save the comparison as markdown.

## Streamlit App

Run the local app from the project root:

```bash
streamlit run src/app.py
```

The app loads both knowledge bases, can generate 5 ideas, lets you paste a
selected idea from radio buttons, choose `text`, `carousel`, or `listicle`, and
generate copy-ready content for review. Generated content can be saved as
markdown in `outputs/`. The app also supports a uniqueness comparison dialog
between generic output and app-generated output.
