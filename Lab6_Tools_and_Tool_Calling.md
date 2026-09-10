# Lab 6 — Tools & Tool Calling with LLMs

---

## Exercise 1 — Order Status Lookup Tool

Build a single tool that looks up the shipping status of an order given an order ID. Bind it to the model and let it answer a natural-language question like *"Where is my order ORD-4521?"*

**Input:** `user_query` (e.g. `"Where is my order ORD-4521?"`)

**Output:** the model's suggested `tool_calls`, the manually executed tool result, and the model's final natural-language answer

**Tool method:** `@tool` (simple lookup, no strict validation needed)

---

## Exercise 2 — Loan EMI Calculator Tool

Build a tool that calculates the monthly EMI (equated monthly installment) given a loan principal, annual interest rate, and tenure in months. The tool must strictly validate that principal and tenure are positive, and interest rate is between 0 and 30.

**Input:** `user_query` (e.g. `"What's my EMI for a 5 lakh loan at 9% for 24 months?"`)

**Output:** the model's suggested `tool_calls`, the manually executed tool result, and the model's final natural-language answer

**Tool method:** `StructuredTool` + Pydantic `args_schema` (fields: `principal: float (gt=0)`, `annual_rate: float (ge=0, le=30)`, `tenure_months: int (gt=0)`)

---

## Exercise 3 — Unit Converter Toolkit (Multiple Tools)

Build two tools — one for temperature conversion (Celsius ↔ Fahrenheit) and one for distance conversion (km ↔ miles) — and bind both to the model in a single call. Ask a question that requires only one of the two tools, and confirm the model picks the correct one.

**Input:** `user_query` (e.g. `"Convert 100 km to miles"`)

**Output:** the model's suggested `tool_calls` (showing which tool it picked), the manually executed result, and the final answer

**Tool method:** `@tool` for both tools

---

## Exercise 4 — Weather-Based Outfit Recommendation (Chained Tools)

Build two tools: `get_weather(city)` which returns the current temperature and conditions for a city, and `recommend_outfit(temperature, conditions)` which returns an outfit suggestion. Since `recommend_outfit` depends on `get_weather`'s output, run the multi-round flow: get the model's first suggestion, execute `get_weather`, feed the result back, then ask the model again for `recommend_outfit`'s arguments. Check whether the model correctly reuses the fetched temperature/conditions or invents its own values.

**Input:** `user_query` (e.g. `"What should I wear today in Mumbai?"`)

**Output:** the model's tool call for `get_weather`, the fetched weather data, the model's second-round tool call for `recommend_outfit` (with whatever arguments it supplies), its result, and the model's final recommendation

**Tool method:** `@tool` for both

---

## Exercise 5 — Async Product Stock Checker

Build a tool that checks whether a product is in stock given a product ID, with both a synchronous and an asynchronous implementation. Demonstrate calling it both ways (`.invoke()` and `.ainvoke()`).

**Input:** `product_id` (direct manual call, no LLM needed for this exercise) and `user_query` (e.g. `"Is product P1023 in stock?"`) for the bound-model version

**Output:** the manual sync call result, the manual async call result, and the full `bind_tools()` flow result for the natural-language query

**Tool method:** `BaseTool` subclass (needs both `_run` and `_arun`)

---

## Exercise 6 — Expense Splitter Tool

Build a tool that splits a total bill amount equally among a given number of people, and returns the amount each person owes. Bind it to the model, and additionally show the same tool being called manually (without the model) with the same inputs to confirm both approaches give the identical result.

**Input:** `user_query` (e.g. `"Split ₹2400 between 4 friends"`) and manual inputs `total_amount`, `num_people`

**Output:** the manual call result, the model's suggested `tool_calls`, the manually executed tool result from the bound flow, and the model's final natural-language answer — compare the manual result and the bound-flow result to confirm they match

**Tool method:** `StructuredTool` + Pydantic `args_schema` (fields: `total_amount: float (gt=0)`, `num_people: int (gt=0)`)

---

## Exercise 7 — Trip Cost Estimator (Multiple Independent Tools, Single Query)

Build three separate tools: `get_flight_cost(origin, destination)`, `get_hotel_cost(city, nights)`, and `get_food_budget(city, days)`. Bind all three to the model in a single `bind_tools()` call. Ask one query that requires the model to call **all three tools** to fully answer, then manually execute each suggested call and feed all three results back before getting the final answer.

**Input:** `user_query` (e.g. `"I'm planning a 3-night trip from Delhi to Goa. What will flights, hotel, and food roughly cost?"`)

**Output:** the model's suggested `tool_calls` (should contain 3 separate calls), each manually executed result, and the model's final combined answer

**Tool method:** `@tool` for all three

---

## Exercise 8 — Health Metrics Toolkit (BMI + Calorie Needs)

Build two tools — `calculate_bmi(weight_kg, height_cm)` and `calculate_daily_calories(weight_kg, height_cm, age, activity_level)` — and group them into a single **Toolkit** class that returns both as a list. Bind the toolkit's tools to the model and ask a query that needs both tools' outputs to give a complete answer.

**Input:** `user_query` (e.g. `"I'm 70kg, 175cm tall, 25 years old, moderately active. What's my BMI and daily calorie need?"`)

**Output:** the toolkit's tool list, the model's suggested `tool_calls` for both tools, each manually executed result, and the model's final combined answer

**Tool method:** `StructuredTool` for both, grouped into a simple `HealthToolkit` class with a `get_tools()` method

---

## Exercise 9 — Smart Meeting Scheduler (Multiple Tools, Partial Use)

Build three tools: `check_calendar_availability(person, date)`, `get_timezone_offset(city)`, and `book_meeting(person, date, time)`. Bind all three, but ask two different queries in the same script — one where the model should call only `check_calendar_availability`, and another where it should call all three in sequence to actually schedule something. Print the `tool_calls` for both queries side by side to show the model only invokes the tools relevant to each query, not all bound tools every time.

**Input:** Two separate `user_query` values — one availability-only question, one full booking request

**Output:** for each query, the model's suggested `tool_calls` (showing different subsets/counts of tools used), the manually executed results, and the final answer

**Tool method:** `@tool` for all three

---

## Exercise 10 — Restaurant Recommendation Assistant (4+ Tools Bound Together)

Build four separate tools: `find_restaurants(cuisine, city)` (returns a list of matching restaurant names), `get_restaurant_rating(restaurant_name)` (returns a rating out of 5), `check_restaurant_open(restaurant_name, day)` (returns whether it's open), and `estimate_cost_for_two(restaurant_name)` (returns an approximate price for two people). Bind all four tools to the model in a single `bind_tools()` call. Ask one query that plausibly requires the model to use several of these tools together to give a complete recommendation, then manually execute whatever it suggests, feed results back, and print the final answer.

**Input:** `user_query` (e.g. `"Suggest a good Italian restaurant in Pune that's open today, with its rating and rough cost for two"`)

**Output:** the model's suggested `tool_calls` (however many tools it decides to use), each manually executed result, and the model's final combined answer

**Tool method:** `@tool` for all four
