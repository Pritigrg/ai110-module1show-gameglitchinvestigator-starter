from logic_utils import check_guess, get_range_for_difficulty, update_score

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# --- Tests targeting fixed bugs ---

def test_hard_range_is_harder_than_normal():
    # Bug: Hard difficulty returned (1, 50), which was *easier* than Normal (1, 100).
    # Fixed to (1, 200).
    _, hard_max = get_range_for_difficulty("Hard")
    _, normal_max = get_range_for_difficulty("Normal")
    assert hard_max > normal_max, (
        f"Hard max ({hard_max}) should be greater than Normal max ({normal_max})"
    )

def test_hard_range_exact_value():
    # Ensures the Hard range is exactly (1, 200), not just "greater than Normal".
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 200

def test_too_high_message_says_go_lower():
    # Bug: when guess > secret the message incorrectly said "Go HIGHER!".
    # Fixed so "Too High" outcome returns a message containing "LOWER".
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message, f"Expected 'LOWER' in message, got: '{message}'"

def test_too_low_message_says_go_higher():
    # Bug: when guess < secret the message incorrectly said "Go LOWER!".
    # Fixed so "Too Low" outcome returns a message containing "HIGHER".
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message, f"Expected 'HIGHER' in message, got: '{message}'"

def test_update_score_deducts_on_too_high():
    # Bug: update_score added points for "Too High" on even attempt numbers.
    # Fixed so any wrong guess always deducts 5 points.
    for attempt in range(1, 6):
        score_before = 100
        score_after = update_score(score_before, "Too High", attempt)
        assert score_after < score_before, (
            f"Score should decrease for 'Too High' on attempt {attempt}, "
            f"got {score_after} (was {score_before})"
        )
