import random
import streamlit as st
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

# FIX: Secret was regenerated on every rerun. I asked Claude how to persist a variable across Streamlit reruns; it introduced session_state here.
if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "game_count" not in st.session_state:
    st.session_state.game_count = 0

if "last_feedback" not in st.session_state:
    st.session_state.last_feedback = None

st.subheader("Make a guess")

# FIX: Range display was hardcoded to "1 and 100". I noticed it didn't match the sidebar; Claude replaced it with dynamic {low} and {high}.
st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}_{st.session_state.game_count}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

# FIX: New Game only reset the secret — input and history persisted. I caught it during play; Claude cleared all state vars and added game_count to force a fresh input key.
if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.status = "playing"
    st.session_state.score = 0
    st.session_state.history = []
    st.session_state.last_feedback = None
    st.session_state.game_count += 1
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.last_feedback:
        kind, msg = st.session_state.last_feedback
        if msg:
            if kind == "won":
                st.balloons()
                st.success(msg)
            elif kind == "lost":
                st.error(msg)
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()


# FIX: Secret was cast to a string on even attempts, making an exact match impossible. Claude identified the type corruption and removed it.
if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.session_state.last_feedback = ("error", err)
    else:
        st.session_state.history.append(guess_int)

        outcome, message = check_guess(guess_int, st.session_state.secret)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.session_state.status = "won"
            st.session_state.last_feedback = ("won", f"You won! The secret was {st.session_state.secret}. Final score: {st.session_state.score}")
        elif st.session_state.attempts >= attempt_limit:
            st.session_state.status = "lost"
            st.session_state.last_feedback = ("lost", f"Out of attempts! The secret was {st.session_state.secret}. Score: {st.session_state.score}")
        else:
            st.session_state.last_feedback = ("hint", message) if show_hint else ("hint", None)

    # FIX: Score and history updated one step behind. I caught this during manual testing; Claude moved all state updates before st.rerun() so the UI reflects each guess immediately.
    st.rerun()

# Display last feedback after rerun
if st.session_state.last_feedback:
    kind, msg = st.session_state.last_feedback
    if msg:
        if kind == "error":
            st.error(msg)
        elif kind == "hint":
            st.warning(msg)

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
