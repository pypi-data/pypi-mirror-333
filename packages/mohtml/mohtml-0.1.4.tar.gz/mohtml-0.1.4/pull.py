import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.youtube.com/@marimo-team/featured")
    page.get_by_role("button", name="Accept all").click()
    page.get_by_role("button", name="Description. The next").click()
    print(page.get_by_role("cell", name="subscribers").text_content())
    print(page.get_by_role("cell", name="views").text_content())

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
