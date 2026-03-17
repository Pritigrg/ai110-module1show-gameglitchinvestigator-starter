# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
  -  When I first ran the game on normal difficulty, the hints were completely misleading - instead of guiding me toward the secret number, they pointed me in the wrong direction. The "New Game" button also didn't work as expected, so I couldn't properly reset and start fresh.

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
1. **Hints were reversed** — Expected the hints to correctly say "go higher" or "go lower" to guide me toward the secret number. Instead, the logic was flipped, giving the opposite direction.


 2. **Difficulty settings were inconsistent** — The sidebar showed different range and attempt information for Easy and Hard modes than what was displayed in the main section. The two sections didn't match, which was confusing.


 3. **New Game button didn't fully reset** — Expected clicking "New Game" to clear everything, including the guess input box and game history. Instead, only the secret number was regenerated — the input field and history were left over from the previous game.


 4. **Score update logic was wrong** — The score wasn't updating correctly. The `−5` / `+5` point logic for "lower" and "higher" hints had a bug, so scores weren't reflecting actual game progress.



---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
 -> claude code
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
 -> AI gave good suggestion in places where I needed to fix like major bugs like fixing the difficulty settings- range, go lower, higher hints, I verified it with both test cases and manual as well
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
->  When I asked Claude to fix the score history logic, it solved part of the problem but introduced a new one — the game displayed "you already won" instead of showing the final score. I caught this through manual testing and had to re-prompt. In another case, while fixing the Developer Debug Info section, Claude unexpectedly changed the UI layout at the bottom of the page, which I hadn't asked for and had to correct.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
-> By using the test cases and checking through the UI. Especially I focused on the negative cases.
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
 -> While playing the game manually, I noticed that the Developer Debug Info section wasn't updating immediately after each guess — it only refreshed after the next input. This revealed a state timing issue: the score and history were being updated one step behind. 
 -> I also discovered that when I asked Claude to generate new test cases, it added new ones without reviewing the existing ones. When I ran the full suite, some of the older tests were failing. I had to read through and modify them to get everything passing. 
- Did AI help you design or understand any tests? How?
  -> I ask AI to be judge itself and ask if the cases it gave was enough - it gave some additional test cases.
  The hard difficulty test was only checking hard > normal, but since the hard range goes up to 200, a guess of 101 would still pass that check incorrectly. Claude added a more precise boundary test to cover that case.
---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
-> In Streamlit, whenever a user interacts with the app — like clicking a button or typing into a text box — the whole script runs again from the beginning. Session state acts like a small memory for the app. It remembers important information between those reruns, such as the current score, previous guesses, or game settings, so that data doesn’t get reset every time the user interacts with the interface.
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
  -> Checking the code properly , i guess the testing habit more.

- What is one thing you would do differently next time you work with AI on a coding task?
  -> I'd write more precise prompts from the start. Being vague led to Claude making assumptions that required extra back-and-forth to undo. 
- In one or two sentences, describe how this project changed the way you think about AI generated code.
 -> AI is a powerful collaborator, but it still needs a human to verify the logic, test the output, and catch the blind spots as of now. The code might look right on the surface but still have subtle bugs — and that's where our own judgment matters most.


