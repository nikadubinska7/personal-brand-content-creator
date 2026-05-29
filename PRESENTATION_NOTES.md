# Personal Brand Content Creator - Presentation Notes

## One-Line Summary

Personal Brand Content Creator is a local AI-powered Streamlit tool that uses a
personal markdown knowledge base to generate LinkedIn content ideas and posts in
a practical, supply-chain-focused voice.

## Problem The App Solves

Generic AI content often sounds broad, polished, and disconnected from real
professional experience.

This tool solves that by grounding content generation in:

- Personal profile and positioning
- Brand voice rules
- Services and professional direction
- Past post examples
- Supply chain and AI use case research

The goal is to create content that sounds like a supply chain operations
professional developing AI consulting and automation skills, not like an
established AI agency or overclaiming consultant.

## Target User

The app is designed for a supply chain operations professional who is building a
personal brand around:

- Practical AI use cases
- Supply chain operations
- Business process automation
- AI agents and workflow support
- Responsible, realistic AI implementation

## Top-Line Features

### 1. Markdown Knowledge Base Loading

The app reads markdown files from two folders:

- `knowledge_base/primary/`
- `knowledge_base/secondary/`

Primary context includes personal information such as profile, services, brand
voice, and past posts.

Secondary context includes supporting industry and business context such as AI
supply chain trends, use cases, pain points, and competitor positioning.

The app keeps these two context types separate so prompts can treat personal
voice and industry knowledge differently.

### 2. Idea Generation

The user can generate 5 LinkedIn post ideas based on the combined knowledge
base.

Each idea includes:

- Working title
- Business or supply chain problem
- Practical AI angle
- Why the idea fits the author's current positioning

The generated ideas are shown as selectable radio options, so the user does not
need to copy and paste an idea manually.

### 3. Format Selection

After selecting an idea, the user can choose the content format:

- Text post
- Carousel
- Listicle

Each format has its own reusable prompt template.

### 4. LinkedIn-Ready Content Generation

The app generates content using OpenAI, while applying local prompt rules for:

- Clear structure
- Practical business examples
- Supply chain specificity
- 5 to 7 hashtags
- Realistic positioning
- Avoiding overclaiming

The text post prompt asks for practical LinkedIn structure: opening line,
problem, business relevance, where AI could help, example, reflection, question,
hashtags, and image prompt.

### 5. Copy-Ready Output

Generated content is shown in the app as a formatted preview.

The app also includes a `Copy post` button so the user can copy the generated
post for LinkedIn review and publishing.

### 6. Output Saving

Generated outputs can be saved locally into the `outputs/` folder as markdown
files.

Saved files include basic metadata such as:

- Output type
- Creation time
- Selected idea

The `outputs/` folder is ignored by git so generated content is not committed by
default.

### 7. PDF Export Foundation

The project includes a basic PDF export module for carousel and listicle content.

This is part of the MVP foundation, but the visual design of PDF exports is
intentionally left for later refinement.

### 8. Uniqueness Evidence

The app includes a uniqueness comparison workflow.

The user can compare:

- Generic AI output
- App-generated output based on the knowledge base

The comparison is shown in a structured table using five metrics:

- Voice alignment
- Supply chain specificity
- Practical AI angle
- Personal positioning fit
- Business relevance

This supports the project goal of showing how the app output differs from
generic ChatGPT-style content.

## Technical Approach

### Local MVP Architecture

The app is intentionally simple and local.

It uses:

- Python
- Streamlit
- Markdown files as the knowledge source
- OpenAI API for generation
- ReportLab for basic PDF export

It does not use:

- Vector search
- Full RAG pipeline
- LinkedIn auto-posting
- Authentication
- Cloud deployment
- Complex external frameworks

### Modular Code Structure

The code is split into small modules:

- `src/document_processor.py` loads markdown files and preserves file metadata.
- `src/knowledge_base.py` separates primary and secondary context.
- `src/prompt_templates.py` loads and renders reusable markdown prompt templates.
- `src/content_pipeline.py` builds prompts and connects content workflows.
- `src/llm_integration.py` handles OpenAI API calls and environment variables.
- `src/output_saver.py` saves generated markdown outputs.
- `src/pdf_generator.py` handles basic PDF export.
- `src/app.py` provides the Streamlit interface.
- `src/main.py` provides CLI checks and generation commands.

### Knowledge Base Approach

The app uses a simple markdown-based knowledge base instead of embeddings or
vector search.

This was chosen because the MVP needs:

- Clear source files
- Easy editing
- Transparent context
- Simple local demo flow
- No unnecessary architecture before the base workflow works

Primary and secondary knowledge are loaded separately to preserve the difference
between personal voice and supporting business context.

### Prompt Engineering Approach

The project uses prompt templates stored in `templates/`.

Each major workflow has its own template:

- Idea generation
- Text post generation
- Carousel generation
- Listicle generation
- Uniqueness comparison

The prompts include brand safety rules, such as avoiding claims like:

- "I help companies implement AI"
- "My clients achieved"
- "Proven framework"
- "Guaranteed results"
- "As an AI implementation expert"

This keeps the output aligned with the author's actual positioning.

### Human Review Workflow

The app is designed to support human review before publishing.

It generates draft content, but the user remains responsible for:

- Reviewing the output
- Checking tone and accuracy
- Editing before publishing
- Deciding whether the content fits their positioning

The app does not publish content automatically.

## Demo Flow

Recommended demo sequence:

1. Open the Streamlit app.
2. Show the knowledge base files loaded from primary and secondary folders.
3. Click `Generate 5 Ideas`.
4. Select one generated idea using the radio buttons.
5. Choose a format: text, carousel, or listicle.
6. Click `Generate Post`.
7. Show the formatted generated post.
8. Use `Copy post` to demonstrate copy-ready output.
9. Save the output as markdown.
10. Open uniqueness evidence and compare generic output vs app output.

## Key Differentiator

The tool does not just ask AI to "write a LinkedIn post."

It combines:

- Personal brand context
- Professional positioning
- Supply chain experience
- AI/business use case context
- Prompt guardrails
- Structured output formats

This makes the output more specific, realistic, and aligned with the author's
professional direction.

## Current MVP Status

Implemented:

- Markdown ingestion
- Primary and secondary knowledge base separation
- Idea generation
- Format selection
- Text, carousel, and listicle prompt generation
- OpenAI generation workflow
- Streamlit interface
- Copy-ready output
- Markdown output saving
- Basic PDF export foundation
- Uniqueness comparison support

Needs further refinement:

- Final UI design polish
- Better PDF visual layout
- Optional image generation
- More output quality tuning based on user review

## Scope Boundaries

The app intentionally does not include:

- LinkedIn auto-posting
- User accounts or authentication
- Cloud deployment
- Vector database or full RAG
- Autonomous trend monitoring
- Claims of established consulting experience

These exclusions keep the project focused on a working, local, demo-ready MVP.

## Suggested Slide Structure

1. Project title and one-line summary
2. Problem: generic AI content
3. Target user and use case
4. Knowledge base approach
5. App workflow
6. Feature overview
7. Technical architecture
8. Prompt and brand safety approach
9. Demo screenshots
10. Uniqueness comparison
11. MVP scope and next steps
