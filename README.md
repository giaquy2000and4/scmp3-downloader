# SoundCloud Downloader

This Python script automates the download of audio files from a SoundCloud downloader website using Selenium and Microsoft Edge.

## Prerequisites

Before running the script, ensure you have the following installed:

-   **Python 3.x:** Download and install from [python.org](https://www.python.org/).
-   **Selenium:** Install using pip: `pip install selenium`.
-   **Microsoft Edge WebDriver:** Download the appropriate WebDriver for your Edge browser version from [Microsoft Edge WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/). Place the `msedgedriver.exe` in a directory included in your system's PATH, or specify the path directly when initializing the WebDriver.
-   **SoundCloud Links:** Have a list of SoundCloud track URLs that you want to download.

## Installation

1.  **Clone or download the repository:**
    ```bash
    git clone [repository_url]
    cd [repository_directory]
    ```
2.  **Install dependencies (if needed):**
    ```bash
    pip install selenium
    ```

## Usage

1.  **Prepare your SoundCloud links:**
    -   Open the `main()` function in the Python script.
    -   Modify the `links` list to include the SoundCloud track URLs you want to download.
    -   Modify the `website_url` variable to the soundcloud downloader website you want to use.
2.  **Configure Download Directory (Optional):**
    -   In the `setup_driver()` function, modify the `download_dir` variable to the directory where you want to save the downloaded files. Default is `D:\\DATA\\testsoundcloud`.
3.  **Run the script:**
    ```bash
    python your_script_name.py
    ```
4.  **Monitor the output:**
    -   The script will print progress messages to the console, including the status of each download.
    -   Downloaded files will be saved in the specified download directory.
5.  **Check the download directory:**
    - After the script has finished running, check the download directory for your downloaded mp3 files.

## Code Explanation

-   **`setup_driver()`:** Initializes the Microsoft Edge WebDriver with download preferences.
-   **`safe_click()`:** Attempts to click an element, handling potential `ElementClickInterceptedException` errors.
-   **`wait_for_element()`:** Waits for an element to be clickable using `WebDriverWait`.
-   **`wait_for_download_complete()`:** Checks for `.crdownload` or `.tmp` files to determine if a download is in progress.
-   **`count_files_in_directory()`:** Counts the number of `.mp3` files in a given directory.
-   **`process_links()`:** Iterates through a list of SoundCloud links, navigates to the downloader website, enters each link, and initiates the download process.
-   **`main()`:** Orchestrates the entire process, including setting up the driver, processing links, and handling errors.

## Important Notes

-   **Website Changes:** The script relies on the structure of the specified SoundCloud downloader website. If the website's layout changes, the script may need to be updated.
-   **Error Handling:** The script includes basic error handling, but you may need to add more robust error handling for specific scenarios.
-   **Download Speed:** Download speed depends on your internet connection and the website's server.
-   **Disclaimer:** Use this script responsibly and respect copyright laws. Only download content that you have the right to download.
-   **Timeout:** The script uses timeout values for waiting on elements and downloads. If you encounter issues, you may need to adjust these values.
-   **CSS and XPATH:** The script tries to find elements using both CSS selectors and XPATH. If one method fails, it tries the other. This increases the robustness of the script.
-   **Audio Quality:** The script attempts to select a specific audio quality. If the element is not found, it continues with the download, assuming the default quality is acceptable.
-   **Browser Close:** The browser will close automatically after the script finishes. There is a 10 second delay before closing so you can see the final state of the browser.
