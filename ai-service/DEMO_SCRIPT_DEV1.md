# Demo Day Script — AI Developer 1

**Role:** AI Developer 1
**Time Allotted:** ~1.5 Minutes
**Goals:** Launch live tool, demonstrate AI features, explain what AI is doing under the hood.

---

## 1. Opening & The Problem (Day 18)
*Stand confidently. Have the application already running.*

**Action:** Show the Architecture slide briefly, then switch to the live tool.
**Script:**
> "Good afternoon. We built the Operational Risk Event Collector to solve a critical problem: risk events are often reported inconsistently, making it hard to identify patterns or take immediate action. Our tool standardizes this process using AI. Let me show you the live tool."

---

## 2. Live Demo — Create Record & Watch AI Respond (Day 18 & Day 20)
**Action:** Click 'Create New Event'. Type in a basic description, e.g., "An employee accidentally emailed a client list to an external vendor." Hit 'Submit'.
**Script:**
> "As I submit this risk event, the backend asynchronously calls our AI microservice. What's happening right now is our Flask service is sanitizing the input, injecting it into a strict prompt template, and asking Groq's LLaMA 3.3 model to structure this event."
*(Wait for AI description to populate on screen)*
> "Here is the structured analysis produced by the AI, giving us immediate, consistent context."

---

## 3. Live Demo — AI Recommend (Day 20)
**Action:** Click the 'AI Recommend' button.
**Script:**
> "Next, we need to know how to fix this. When I click 'Recommend', our AI service doesn't just guess—it queries a ChromaDB knowledge base loaded with operational risk policies using Sentence Transformers, and then generates exactly three actionable mitigation strategies. As you can see, we have clear action types, owners, and priority levels assigned instantly."

---

## 4. Live Demo — Generate Report (Day 20)
**Action:** Select 3-4 events from the dashboard and click 'Generate Report'.
**Script:**
> "Finally, at the end of the month, the Chief Risk Officer needs a summary. I select these events and click 'Generate Report'. The AI synthesizes the selected data into a comprehensive executive summary with key themes. This saves hours of manual reporting work while ensuring regulatory readiness."

---

## 5. Handoff
*Transition to AI Developer 2.*
**Script:**
> "I'll now hand it over to my colleague to explain our tech stack and the security measures we implemented to protect this data."
