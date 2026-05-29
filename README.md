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
combined context. This step does not call the OpenAI API.
