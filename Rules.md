# Rules.md

## Core Build Rules

1. Build the MVP first.
2. Keep the app simple, local, and demo-ready.
3. Use Python and Streamlit.
4. Use markdown files as the knowledge source.
5. Do not implement vector search or full RAG unless the MVP is complete.
6. Do not add unnecessary frameworks.
7. Keep code modular and readable.
8. Handle errors clearly.
9. Update documentation when behavior changes.
10. Never commit secrets.

## Scope Rules

The MVP includes:
- markdown ingestion
- primary and secondary knowledge base loading
- idea generation
- format selection
- text post generation
- carousel content generation
- listicle content generation
- PDF export for carousel/listicle
- copy-ready Streamlit output
- output saving
- basic uniqueness evidence support

The MVP excludes:
- LinkedIn auto-posting
- user authentication
- cloud deployment
- advanced analytics dashboard
- full vector database/RAG
- autonomous web trend monitoring
- production-grade design system

## Content Positioning Rules

The user is not yet an established AI consultant.

Generated content must sound like:
- a supply chain operations professional
- developing AI consulting and integration skills
- learning publicly
- building prototypes
- analyzing practical AI use cases
- connecting AI to real business workflows

Generated content must not sound like:
- an established AI agency
- a senior AI implementation expert
- a consultant with proven client results
- a vendor promising transformation

## Forbidden Content Claims

Do not generate claims like:
- “I help companies implement AI”
- “My clients achieved”
- “My proven framework”
- “Guaranteed ROI”
- “We transform supply chains”
- “As an AI implementation expert”
- “I have implemented this across multiple companies”

Use safer alternatives:
- “I am exploring”
- “I built a prototype”
- “This made me think”
- “A practical starting point could be”
- “This use case shows”
- “This could support teams by”

## Brand Voice Rules

The voice should be:
- practical
- analytical
- clear
- curious
- structured
- business-focused
- operational
- realistic
- human
- implementation-focused

Avoid:
- hype
- buzzwords
- vague transformation language
- corporate article tone
- generic motivational language
- unsupported claims
- too much polish

## LinkedIn Output Rules

Each post should include:
- strong opening line
- short paragraphs
- clear business problem
- practical AI angle
- operational example
- reflection or soft question
- 5–7 hashtags

Use LinkedIn-safe symbols only where useful.

Avoid excessive emojis.

## PDF Output Rules

Carousel PDFs:
- one main idea per slide
- strong title slide
- simple layout
- readable text
- practical takeaway
- no crowded slides

Listicle PDFs:
- clear title
- numbered points
- short explanations
- practical business relevance
- clean layout

## Coding Rules

Use:
- type hints where helpful
- clear function names
- small modules
- readable error messages
- `pathlib` for paths
- `.env` for environment variables

Avoid:
- hardcoded absolute paths
- hardcoded API keys
- large monolithic files
- silent failures
- unnecessary dependencies

## Git Rules

Do not commit:
- `.env`
- API keys
- generated output files unless intentionally needed for demo
- cache folders
- virtual/conda environment files

Commit:
- source code
- knowledge base markdown files
- prompt templates
- documentation
- requirements files
- project management evidence if stored in repo

## Testing Rules

Before marking a feature done:
- run the app locally
- test the relevant button/action
- check output quality manually
- check for overclaiming
- check that errors are readable
- update Trello and prompt tracking if relevant