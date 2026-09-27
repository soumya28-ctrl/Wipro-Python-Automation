import json
import os
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ============================================================
# READ TEST DATA
# ============================================================

with open("test_data.json", "r") as file:
    data = json.load(file)

URL = data["url"]
USERNAME = data["username"]
PASSWORD = data["password"]
PRODUCT = data["product"]
QUANTITY = data["quantity"]


# ============================================================
# SCREENSHOT FUNCTION
# ============================================================

def take_screenshot(driver, name):

    os.makedirs("screenshots", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    path = f"screenshots/{name}_{timestamp}.png"

    driver.save_screenshot(path)

    print(f"Screenshot saved: {path}")


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    print("Starting Selenium automation...")

    # --------------------------------------------------------
    # 1. LAUNCH BROWSER
    # --------------------------------------------------------

    driver = webdriver.Chrome()

    driver.maximize_window()

    wait = WebDriverWait(driver, 10)

    driver.get(URL)

    print("Browser launched")

    take_screenshot(driver, "01_home_page")


    # --------------------------------------------------------
    # 2. LOGIN
    # --------------------------------------------------------

    print("Opening login page...")

    my_account = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//span[contains(text(),'My Account')]")
        )
    )

    my_account.click()

    login_link = wait.until(
        EC.element_to_be_clickable(
            (By.LINK_TEXT, "Login")
        )
    )

    login_link.click()

    take_screenshot(driver, "02_login_page")

    print("Entering login details...")

    email = wait.until(
        EC.visibility_of_element_located(
            (By.ID, "input-email")
        )
    )

    email.send_keys(USERNAME)

    password = driver.find_element(
        By.ID,
        "input-password"
    )

    password.send_keys(PASSWORD)

    login_button = driver.find_element(
        By.XPATH,
        "//input[@value='Login']"
    )

    login_button.click()

    print("Login completed")

    take_screenshot(driver, "03_after_login")


    # --------------------------------------------------------
    # 3. SEARCH PRODUCT
    # --------------------------------------------------------

    print(f"Searching for: {PRODUCT}")

    search_box = wait.until(
        EC.visibility_of_element_located(
            (By.NAME, "search")
        )
    )

    search_box.send_keys(PRODUCT)

    search_button = driver.find_element(
        By.CSS_SELECTOR,
        "button.btn.btn-default.btn-lg"
    )

    search_button.click()

    print("Product search completed")

    take_screenshot(driver, "04_product_search")


    # --------------------------------------------------------
    # 4. ADD PRODUCT TO CART
    # --------------------------------------------------------

    print("Adding product to cart...")

    add_to_cart = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//button[contains(@onclick,'cart.add')]"
            )
        )
    )

    add_to_cart.click()

    print("Product added to cart")

    take_screenshot(driver, "05_product_added")


    # --------------------------------------------------------
    # 9. HANDLE ALERT
    # --------------------------------------------------------

    try:

        alert = WebDriverWait(driver, 3).until(
            EC.alert_is_present()
        )

        print("Alert found:", alert.text)

        alert.accept()

        print("Alert accepted")

    except:

        print("No alert found")


    # --------------------------------------------------------
    # 6. OPEN CART
    # --------------------------------------------------------

    print("Opening cart...")

    cart_button = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//div[@id='cart']//button"
            )
        )
    )

    cart_button.click()

    view_cart = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//strong[contains(text(),'View Cart')]"
            )
        )
    )

    view_cart.click()

    print("Cart opened")

    take_screenshot(driver, "06_cart")


    # --------------------------------------------------------
    # VERIFY PRODUCT
    # --------------------------------------------------------

    product_name = wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//div[@class='table-responsive']//td[2]"
            )
        )
    )

    actual_product = product_name.text

    print("Product in cart:", actual_product)

    if PRODUCT.lower() in actual_product.lower():

        print("Product verification PASSED")

    else:

        print("Product verification FAILED")


    # --------------------------------------------------------
    # 5. UPDATE QUANTITY
    # --------------------------------------------------------

    print(f"Updating quantity to {QUANTITY}...")

    quantity_box = wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//input[contains(@name,'quantity')]"
            )
        )
    )

    quantity_box.clear()

    quantity_box.send_keys(str(QUANTITY))

    update_button = driver.find_element(
        By.XPATH,
        "//button[@data-original-title='Update']"
    )

    update_button.click()

    print("Quantity updated")

    take_screenshot(driver, "07_quantity_updated")


    # --------------------------------------------------------
    # VERIFY QUANTITY
    # --------------------------------------------------------

    quantity_box = wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//input[contains(@name,'quantity')]"
            )
        )
    )

    actual_quantity = quantity_box.get_attribute("value")

    print("Expected quantity:", QUANTITY)
    print("Actual quantity:", actual_quantity)

    if actual_quantity == str(QUANTITY):

        print("Quantity verification PASSED")

    else:

        print("Quantity verification FAILED")


    # --------------------------------------------------------
    # FINAL SCREENSHOT
    # --------------------------------------------------------

    take_screenshot(driver, "08_final_cart")

    print("")
    print("======================================")
    print("E-COMMERCE AUTOMATION COMPLETED")
    print("======================================")


    # --------------------------------------------------------
    # CLOSE BROWSER
    # --------------------------------------------------------

    driver.quit()

    print("Browser closed")


# ============================================================
# RUN PROGRAM
# ============================================================

if __name__ == "__main__":
    main()
