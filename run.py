import glob
import os
import time

from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def setup_driver():
    """Set up the Edge WebDriver with appropriate options."""
    # Define Edge options
    edge_options = Options()

    # Set download directory to the specified path
    download_dir = "D:\\DATA\\testsoundcloud"
    os.makedirs(download_dir, exist_ok=True)
    print(f"Files will be saved to: {download_dir}")

    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    edge_options.add_experimental_option("prefs", prefs)

    # Initialize the Edge driver
    driver = webdriver.Edge(options=edge_options)
    driver.maximize_window()
    return driver, download_dir


def safe_click(driver, element, timeout=2):
    """Attempt to click an element safely, handling possible issues."""
    try:
        # Scroll element into view
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        time.sleep(0.5)  # Reduced wait time for scrolling

        # Try JavaScript click if normal click fails
        try:
            element.click()
        except ElementClickInterceptedException:
            driver.execute_script("arguments[0].click();", element)

        return True
    except Exception as e:
        print(f"Click failed: {e}")
        return False


def wait_for_element(driver, locator_type, locator, timeout=10):
    """Wait for an element to be clickable with reduced timeout."""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((locator_type, locator))
        )
        return element
    except Exception:
        return None


def wait_for_download_complete(download_dir, timeout=60):
    """Wait for download to complete by checking for .crdownload or .tmp files."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        # Check if any .crdownload or .tmp files exist in the download directory
        downloading_files = glob.glob(os.path.join(download_dir, "*.crdownload"))
        downloading_files.extend(glob.glob(os.path.join(download_dir, "*.tmp")))

        if not downloading_files:
            # Wait a bit to make sure we're not checking between files
            time.sleep(1)
            # Check again
            downloading_files = glob.glob(os.path.join(download_dir, "*.crdownload"))
            downloading_files.extend(glob.glob(os.path.join(download_dir, "*.tmp")))

            if not downloading_files:
                # If still no downloading files, assume download is complete
                return True

        print("Download in progress... waiting.")
        time.sleep(2)

    # If we reach here, timeout occurred
    print("Download wait timed out!")
    return False


def count_files_in_directory(directory):
    """Count number of mp3 files in the directory."""
    return len(glob.glob(os.path.join(directory, "*.mp3")))


def process_links(driver, links, website_url, download_dir):
    """Process each link in the provided list."""
    for i, link in enumerate(links):
        try:
            print(f"\nProcessing link {i + 1}/{len(links)}: {link}")

            # Count files before downloading
            files_before = count_files_in_directory(download_dir)

            # Navigate to the website
            driver.get(website_url)
            time.sleep(3)  # Slightly increased wait time for page load

            # Find and fill the search box - try XPath first, then CSS
            search_box = wait_for_element(driver, By.XPATH, "/html/body/div[7]/div[3]/div/form/div/input")
            if not search_box:
                search_box = wait_for_element(driver, By.CSS_SELECTOR, "input[type='text']")

            if search_box:
                search_box.clear()
                search_box.send_keys(link)
                print("Entered link in search box")
            else:
                print("Failed to find search box")
                continue

            # Click search button - try XPath first, then CSS
            search_button = wait_for_element(driver, By.XPATH, "/html/body/div[7]/div[3]/div/form/div/button")
            if not search_button:
                search_button = wait_for_element(driver, By.CSS_SELECTOR, "button[type='submit']")

            if search_button and safe_click(driver, search_button):
                print("Clicked search button")
            else:
                print("Failed to find or click search button")
                continue

            # Wait for search results to load
            time.sleep(5)  # Increased wait time to ensure results load

            # Click download button - try XPath first, then CSS
            download_button = wait_for_element(driver, By.XPATH,
                                               "/html/body/div[7]/div[6]/div/div/div[1]/div/div[2]/div[1]/div[1]/div/a")
            if not download_button:
                # Try multiple CSS selectors that are commonly used for download buttons
                for selector in ["a.download-button", "a.btn-download", "a[href*='download']", ".download", "a.btn"]:
                    download_button = wait_for_element(driver, By.CSS_SELECTOR, selector, timeout=3)
                    if download_button:
                        break

            if download_button and safe_click(driver, download_button):
                print("Clicked download button")
            else:
                print("Failed to find or click download button")
                continue

            # Wait for quality options to appear
            time.sleep(5)  # Increased wait time

            # Select audio quality - try XPath first, then CSS
            audio_quality = wait_for_element(driver, By.XPATH,
                                             "/html/body/div[7]/div[6]/div/div/div[1]/div/div[2]/div[1]/div[1]/ul/li[4]/button")
            if not audio_quality:
                # Try multiple CSS selectors that might relate to audio quality
                for selector in ["button.quality-button", "button[data-quality='mp3']", "li:nth-child(4) button",
                                 ".quality-selector button"]:
                    audio_quality = wait_for_element(driver, By.CSS_SELECTOR, selector, timeout=3)
                    if audio_quality:
                        break

            if audio_quality and safe_click(driver, audio_quality):
                print("Selected audio quality")
            else:
                print("Failed to find or click audio quality button - continuing anyway")
                # Continue anyway as the download might have started

            # Wait for download to begin
            print("Waiting for download to start...")
            time.sleep(8)  # Increased wait time for download to start

            # Wait for download to complete
            print("Waiting for download to complete...")
            wait_for_download_complete(download_dir)

            # Count files after downloading
            files_after = count_files_in_directory(download_dir)

            if files_after > files_before:
                print(f"Download confirmed! New file detected in {download_dir}")
            else:
                print("No new MP3 file detected. Download may have failed or saved in a different format.")

            print(f"Completed processing link {i + 1}")

        except Exception as e:
            print(f"Error processing link {i + 1}: {e}")
            # Continue with the next link even if there's an error
            continue


def main():
    # SoundCloud downloader website URL
    website_url = "https://soundcloudmp3.cc/"  # Example downloader site, replace with actual site

    # List of links to process - using your actual SoundCloud links
    links = [
        "https://soundcloud.com/quanmyn/wake-me-up-2022-vavh-remix-hd?si=b341c8ab845e46b6b3fa3acc741f5ff7&utm_source=clipboard&utm_medium=text&utm_campaign=social_sharing",
        "https://soundcloud.com/hay-nhac-269919328/amore-mio-vavh-remix-reup?si=5d60e500552241a9ad2646f606de8364&utm_source=clipboard&utm_medium=text&utm_campaign=social_sharing",
        # Add more links as needed
    ]

    # Set up the driver
    driver, download_dir = setup_driver()

    try:
        # Process all links
        process_links(driver, links, website_url, download_dir)
        print("\nAll links processed successfully!")
        print(f"Check your downloads in: {download_dir}")

        # Keep browser open for additional time after completion
        print("Waiting an additional 10 seconds before closing...")
        time.sleep(10)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Clean up - close the browser
        driver.quit()


if __name__ == "__main__":
    main()
