# Task 1: Prompt frameworks for Text-to-SQL

## Task and database context

The prompts are intended for the restaurant Text-to-SQL benchmark in Task 2. The supplied question file contains 155 question/result pairs. The questions cover restaurant type and city filters, rating thresholds, address/street searches, broader regions, best/highest-rated requests, named-restaurant lookups, and some questions with unrelated conversational distractions. One question is not a restaurant/database request.

The database schema is:

- `RESTAURANT(ID, NAME, FOOD_TYPE, CITY_NAME, RATING)`
- `LOCATION(RESTAURANT_ID, HOUSE_NUMBER, STREET_NAME, CITY_NAME)`
- `GEOGRAPHIC(CITY_NAME, COUNTY, REGION)`

The schema marks foreign-key fields but does not specify their target columns. The prompts therefore assume that `LOCATION.RESTAURANT_ID` references `RESTAURANT.ID`, and that `RESTAURANT.CITY_NAME` references `GEOGRAPHIC.CITY_NAME` for county/region filters; these joins are inferred from matching column names and the benchmark's query types, not explicitly documented as foreign-key targets. Address searches use `LOCATION`. `HOUSE_NUMBER` is numeric.

All three prompts include the same seven few-shot examples. They cover city/rating filtering, food type plus city/rating, address searches, region joins, highest-rated requests, named-restaurant lookups, and a non-database question that requires the prescribed empty-result fallback. The examples use plausible values from the supplied restaurant domain, but their question wording is newly written rather than copied verbatim from the benchmark questions.

A key distinction for Task 2 is that a valid restaurant query can legitimately return zero rows. The fallback `SELECT NULL WHERE 1 = 0;` is reserved for requests that cannot be answered using the supplied schema, such as an unrelated non-restaurant question. The prompts also tell the model not to use `DISTINCT` automatically, because the evaluator compares results as multisets and therefore counts duplicates.

## RTF (Role – Task – Format)

Source: [RTF framework](https://frompting.com/frameworks/rtf)

RTF separates the model's role, task, and required output format. This is a natural fit for a constrained Text-to-SQL task: it establishes the model as a query generator, specifies the transformation, and makes the SQL-only output requirement explicit. The shared examples demonstrate the same common query patterns tested in Task 2. I expect RTF's direct organization to help maintain concise, consistently formatted SQL and avoid explanatory text in outputs.

## ICIO (Instruction – Context – Input – Output)

Source: [ICIO framework](https://frompting.com/frameworks/icio)

ICIO separates the instruction, task context, variable input, and expected output. That organization is useful when the same prompt is reused for many questions: the schema, relationships, general rules, and examples remain fixed, while the natural-language question changes. I expect the explicit separation of input and output to support consistent query generation and compliance with the evaluator's format requirements.

## CRISP (Context – Role – Intent – Style – Parameters)

Source: [CRISP framework](https://frompting.com/frameworks/crisp)

CRISP provides a more detailed brief by identifying the context, role, intent, style, and parameters. This structure gives a place to state the evaluation setting, clarify the required result columns, and specify how to handle distractor text and SQL constraints. Its added structure may help with more complicated combinations of region, address, food type, and rating. However, it could also be more verbose than necessary for this narrowly defined task. The Task 2 experiment will test these possibilities.

## Expected comparison and experimental controls

The prompts share the same schema, joins, general rules, seven examples, fallback behavior, and SQL-only output format. They differ primarily in how those instructions are organized according to RTF, ICIO, and CRISP. This is intended to make framework organization the main planned difference rather than giving one prompt different demonstrations or database knowledge.

The expectations above are hypotheses, not measured findings. In Task 2, all three prompts should be tested on the same 155 questions, using the same model and separate sessions as required by the assignment. Store the raw SQL outputs and prompt/model metadata, measure inference time consistently, and evaluate each prediction with the supplied evaluator. No framework should be described as better until the results have been measured.
