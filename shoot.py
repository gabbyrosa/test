import glob, os
from playwright.sync_api import sync_playwright

# find the chromium executable Playwright shipped
cands = glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome")
exe = cands[0] if cands else None

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=exe, args=["--no-sandbox"])
    for scheme in ("dark", "light"):
        page = browser.new_page(viewport={"width": 960, "height": 1200},
                                color_scheme=scheme, device_scale_factor=2)
        page.goto("file:///home/user/test/birth_chart.html")
        page.wait_for_timeout(700)
        page.screenshot(path=f"/home/user/test/preview_{scheme}.png", full_page=True)
        print("shot", scheme)
    browser.close()
