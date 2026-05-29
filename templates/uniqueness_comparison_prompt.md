# Uniqueness Comparison Prompt

You are evaluating whether app-generated LinkedIn content is more aligned with
the author's knowledge base than a generic AI output.

Use the primary context to judge voice, credibility level, positioning, and
overclaiming risk. Use the secondary context to judge business and supply chain
specificity.

## Primary Context

{{primary_context}}

## Secondary Context

{{secondary_context}}

## Generic Output

{{generic_output}}

## App Output

{{app_output}}

## Task

Create concise uniqueness evidence for project documentation.

Return:

1. A short summary of the comparison.
2. A markdown table comparing the outputs using exactly these metrics:
   - Voice alignment
   - Supply chain specificity
   - Practical AI angle
   - Personal positioning fit
   - Business relevance
3. A short note on overclaiming risks found in either output.
4. A final recommendation for what to improve before publishing.

Use this table structure:

| Metric | Generic output | App output | Stronger output | Notes |
|---|---|---|---|---|

Keep the analysis practical, specific, and business-focused.
