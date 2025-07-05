import re
from playwright.sync_api import Page, expect


def test_homepage_has_title_and_form(page: Page):
    page.goto("http://127.0.0.1:8000")

    # Expect a title "Big Beautiful Bill"
    expect(page).to_have_title(re.compile("Big Beautiful Bill"))

    # create a locator
    ask_button = page.get_by_role("button", name="Ask")

    # Expect an attribute "to be strictly equal" to the value.
    expect(ask_button).to_have_attribute("type", "submit")

def test_asking_a_question(page: Page):
    page.goto("http://127.0.0.1:8000")

    # Find the input field and type a question
    page.get_by_placeholder("Ask a question about the bill...").fill("What is the bill about?")

    # Click the "Ask" button
    page.get_by_role("button", name="Ask").click()

    # Wait for the answer to appear
    answer_element = page.locator("#answer-container")
    expect(answer_element).to_be_visible()
    expect(answer_element).not_to_be_empty()
