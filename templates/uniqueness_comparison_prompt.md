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
2. 3 to 5 specific differences between the generic output and the app output.
3. A short assessment of whether the app output better matches the author's
   current positioning.
4. Any overclaiming risks found in either output.
5. A final recommendation for what to improve before publishing.

Keep the analysis practical, specific, and business-focused.
