# Project Requirements

## 1. Project Summary

- Project name: Personal Brand Content Creator
- Project type: AI Content Creator — Personal Brand Content Creator
- Target user: A supply chain operations professional currently developing AI consulting and integration capability
- Problem we are solving: Generic AI content often sounds repetitive, vague, and disconnected from real professional experience. This project creates a content generation tool that uses a personal knowledge base and AI-in-supply-chain research to generate LinkedIn content ideas, posts, carousel outlines, and listicle content in a practical, realistic, personal voice.
- Primary business goal: Support consistent LinkedIn content creation around AI in supply chain, business process automation, responsible AI usage, and practical AI implementation.
- Success criteria:
  - The app reads markdown files from both primary and secondary knowledge bases.
  - The app generates 5 relevant post ideas.
  - The user can choose a post format: text, carousel, or listicle.
  - The app generates LinkedIn-ready content using the user's voice and positioning.
  - The app includes 5–7 relevant hashtags.
  - The app can export carousel/listicle content as PDF.
  - The project demonstrates uniqueness compared with generic ChatGPT output.

## 2. Scope

### Must Have

- [ ] Read and process markdown files from `knowledge_base/primary/`
- [ ] Read and process markdown files from `knowledge_base/secondary/`
- [ ] Generate 5 LinkedIn post ideas based on both knowledge bases
- [ ] Allow user to select content format: text, carousel, or listicle
- [ ] Generate LinkedIn-ready text posts
- [ ] Generate carousel caption and carousel PDF
- [ ] Generate listicle caption and listicle PDF
- [ ] Generate 5–7 relevant hashtags for each post
- [ ] Provide copy-ready post text in the app interface
- [ ] Use reusable prompt templates
- [ ] Include human review before publishing
- [ ] Provide uniqueness comparison evidence
- [ ] Maintain prompt tracking and change log

### Should Have

- [ ] Generate an image prompt for every text post
- [ ] Save generated outputs into the `outputs/` folder
- [ ] Provide a simple Streamlit interface with buttons
- [ ] Include clear README setup instructions
- [ ] Include error handling for missing files or missing API key

### Could Have

- [ ] Generate actual images for text posts
- [ ] Add article-summary mode for pasted web articles
- [ ] Store generated post history
- [ ] Add local embeddings or vector search
- [ ] Add automated evaluation of brand alignment

### Out of Scope

- Automated posting to LinkedIn
- User login or authentication
- Cloud deployment
- Full RAG/vector database as a required feature
- Fully autonomous content publishing
- Claiming established consulting experience or client results

## 3. Functional Requirements

| ID | Requirement | Acceptance Criteria | Trello Card |
|----|-------------|---------------------|-------------|
| FR-001 | The app can ingest markdown files from both knowledge bases. | Given valid markdown files in primary and secondary folders, when the app runs, then the content is loaded and available for prompts. | TBD |
| FR-002 | The app can separate primary and secondary context. | Given both knowledge bases, when prompts are built, then personal voice/profile context and industry context are handled separately. | TBD |
| FR-003 | The app can generate 5 post ideas. | Given loaded context, when the user clicks “Generate 5 Ideas,” then exactly 5 relevant ideas are returned. | TBD |
| FR-004 | The user can select a content format. | Given generated ideas, when the user selects text, carousel, or listicle, then the selected format is passed into the generation pipeline. | TBD |
| FR-005 | The app can generate a text LinkedIn post. | Given a selected idea and text format, when “Generate Post” is clicked, then the app produces a structured LinkedIn post with 5–7 hashtags and an image prompt. | TBD |
| FR-006 | The app can generate carousel content. | Given a selected idea and carousel format, when “Generate Post” is clicked, then the app produces a caption and a PDF carousel. | TBD |
| FR-007 | The app can generate listicle content. | Given a selected idea and listicle format, when “Generate Post” is clicked, then the app produces a caption and a PDF listicle. | TBD |
| FR-008 | The app keeps the voice realistic and non-overclaiming. | Generated content must avoid phrases such as “I help companies,” “my clients,” “proven framework,” or claims of established consulting expertise. | TBD |
| FR-009 | The app supports copy-ready output. | Generated captions/posts are shown in a text area so the user can copy them. | TBD |
| FR-010 | The project includes uniqueness evidence. | At least one example compares generic ChatGPT output with the app output and explains the differences. | TBD |
| FR-011 | The app saves generated files. | PDFs and generated text outputs are saved into the `outputs/` folder. | TBD |
| FR-012 | The app handles errors clearly. | If API key or knowledge base files are missing, the app shows a clear error message instead of crashing silently. | TBD |

## 4. Non-Functional Requirements

- Reliability: The app should handle missing files, empty folders, and missing API keys with clear messages.
- Privacy and API-key handling: API keys must be stored in `.env` and excluded from GitHub through `.gitignore`.
- Maintainability: Code should be modular, with separate files for document processing, knowledge base handling, prompt templates, LLM integration, pipeline logic, and PDF generation.
- Usability: The interface should be simple enough to demo clearly: generate ideas, choose format, generate post, copy/download output.
- Content quality: Outputs should be practical, structured, LinkedIn-ready, and aligned with the user’s personal voice.
- Brand safety: The app must avoid overclaiming consulting experience or implying client results that do not exist.

## 5. Kanban / Project Management

- Board name: ACFT0520 - Project 2 - Personal Brand Content Creator
- Board link, if shareable: TBD
- Workflow columns:
  - Backlog
  - Ready
  - In Progress
  - Review / Testing
  - Done
- WIP limit:
  - Maximum 2 cards in “In Progress” at the same time
- Definition of Done:
  - Code runs locally
  - Requirement acceptance criteria are met
  - Related documentation is updated
  - Human review completed
  - No secrets committed
- Review cadence:
  - Planning checkpoint
  - Midpoint checkpoint
  - Final checkpoint

## 6. AI Coding-Agent Rules

- AI coding agent used: Codex / VSCode agent
- The agent is allowed to:
  - Generate initial code drafts
  - Refactor modules
  - Suggest tests
  - Debug errors
  - Improve documentation
  - Propose prompt templates
- The agent is not allowed to:
  - Commit API keys or private data
  - Remove knowledge base files without approval
  - Change project scope without updating this file
  - Add complex RAG/vector search before the MVP works
  - Make unsupported claims in generated LinkedIn content
- Human review process:
  - Review generated code before running
  - Test each feature manually
  - Check content against brand voice rules
  - Check that outputs do not overclaim consulting experience
  - Update prompt tracking log after meaningful agent use
- Secrets protection:
  - Store API keys only in `.env`
  - Keep `.env` in `.gitignore`
  - Never paste real API keys into prompts, commits, screenshots, or documentation

## 7. Prompt Tracking Log

| Date | Tool / Agent | Prompt Goal | Prompt Summary | Output Used? | Human Review Notes | Related Commit / PR |
|------|--------------|-------------|----------------|--------------|--------------------|---------------------|
| TBD | ChatGPT | Project planning | Defined project structure, MVP scope, knowledge base split, and required files. | Yes | Reviewed against project brief and adjusted to personal-brand topic. | TBD |
| TBD | Codex / VSCode agent | TBD | TBD | TBD | TBD | TBD |

## 8. Change Log

| Date | Requirement / Decision Changed | Why It Changed | Approved By |
|------|-------------------------------|----------------|-------------|
| TBD | Initial MVP defined without required vector database | Course brief says markdown context is sufficient and vector/RAG is optional. | Project owner |
| TBD | Image generation moved to Should Have / Could Have depending on time | Core grading depends more on document processing, LLM integration, uniqueness, and documentation. | Project owner |
EOF