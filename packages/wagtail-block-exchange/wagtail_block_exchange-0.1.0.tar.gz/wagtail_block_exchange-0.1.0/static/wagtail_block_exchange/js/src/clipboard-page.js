/**
 * Wagtail Block Exchange - Clipboard Page Functionality
 *
 * This module handles all interactions on the Block Clipboard page,
 * including paste and delete operations.
 */

import { deleteClipboardItem, pasteBlockToPage } from "./utils/api-client";
import { notify } from "./utils/notifications";

class ClipboardPage {
  constructor() {
    this.initialized = false;
  }

  /**
   * Initialize clipboard page functionality
   */
  initialize() {
    // Skip if not on clipboard page
    if (!this.isClipboardPage()) {
      return;
    }

    console.log("🔍 Block Exchange: Initializing clipboard page");

    // Add event listeners
    this.setupDeleteButtons();
    this.setupPasteButtons();

    this.initialized = true;
  }

  /**
   * Check if current page is the clipboard page
   */
  isClipboardPage() {
    try {
      const isClipboard = window.location.pathname.includes(
        "/admin/block-exchange/clipboard/"
      );
      console.log("🔍 Block Exchange: Is clipboard page?", isClipboard);
      return isClipboard;
    } catch (err) {
      console.error(
        "🔍 Block Exchange: Error checking if clipboard page:",
        err
      );
      return false;
    }
  }

  /**
   * Set up delete button click handlers
   */
  setupDeleteButtons() {
    const deleteButtons = document.querySelectorAll(
      ".delete-clipboard-item-button"
    );
    console.log(
      `🔍 Block Exchange: Found ${deleteButtons.length} delete buttons`
    );

    deleteButtons.forEach((button) => {
      button.addEventListener("click", this.handleDeleteButtonClick.bind(this));
    });
  }

  /**
   * Set up paste button click handlers
   */
  setupPasteButtons() {
    const pasteButtons = document.querySelectorAll(".paste-block-button");
    console.log(
      `🔍 Block Exchange: Found ${pasteButtons.length} paste buttons`
    );

    pasteButtons.forEach((button) => {
      button.addEventListener("click", this.handlePasteButtonClick.bind(this));
    });
  }

  /**
   * Handle delete button clicks
   * @param {Event} e - Click event
   */
  handleDeleteButtonClick(e) {
    e.preventDefault();
    const button = e.currentTarget;
    const clipboardId = button.getAttribute("data-clipboard-id");

    if (!clipboardId) {
      notify.error("Missing clipboard item ID");
      return;
    }

    console.log(
      "🔍 Block Exchange: Delete button clicked for item",
      clipboardId
    );

    // Confirm before deleting
    if (!confirm("Are you sure you want to delete this clipboard item?")) {
      return;
    }

    // Find the CSRF token
    const csrfToken = document.querySelector(
      'input[name="csrfmiddlewaretoken"]'
    ).value;

    // Disable the button
    button.disabled = true;
    button.textContent = "Deleting...";

    // Send delete request
    deleteClipboardItem(clipboardId, csrfToken)
      .then((data) => {
        if (data.success) {
          notify.success("Clipboard item deleted");

          // Remove the item from the DOM
          const clipboardItem = document.querySelector(
            `.clipboard-item[data-clipboard-id="${clipboardId}"]`
          );
          if (clipboardItem) {
            clipboardItem.remove();
          }

          // Check if there are no items left
          const remainingItems = document.querySelectorAll(".clipboard-item");
          if (remainingItems.length === 0) {
            // Show empty message
            const listContainer = document.querySelector(".clipboard-list");
            if (listContainer) {
              listContainer.innerHTML = `
                                <div class="clipboard-empty">
                                    <p>You haven't copied any blocks to your clipboard yet.</p>
                                    <p>To copy a block, edit a page and click the 'Copy to Clipboard' button in the block menu.</p>
                                </div>
                            `;
            }
          }
        } else {
          notify.error(
            "Failed to delete clipboard item: " +
              (data.error || "Unknown error")
          );

          // Re-enable the button
          button.disabled = false;
          button.textContent = "Remove";
        }
      })
      .catch((error) => {
        notify.error("Error deleting clipboard item: " + error.message);

        // Re-enable the button
        button.disabled = false;
        button.textContent = "Remove";
      });
  }

  /**
   * Handle paste button clicks
   * @param {Event} e - Click event
   */
  handlePasteButtonClick(e) {
    e.preventDefault();
    const button = e.currentTarget;
    const clipboardId = button.getAttribute("data-clipboard-id");

    if (!clipboardId) {
      notify.error("Missing clipboard item ID");
      return;
    }

    console.log(
      "🔍 Block Exchange: Paste button clicked for item",
      clipboardId
    );
    this.openPageChooserForPaste(clipboardId);
  }

  /**
   * Open the page chooser dialog for pasting
   * @param {string} clipboardId - The clipboard item ID
   */
  openPageChooserForPaste(clipboardId) {
    // If Wagtail has a page chooser, use it
    if (window.ModalWorkflow) {
      window.ModalWorkflow({
        url: window.chooserUrls.pageChooser,
        onload: {
          choose: function (pageData) {
            this.pasteBlockToChosenPage(clipboardId, pageData.id);
          }.bind(this),
        },
      });
    } else {
      // Fall back to a simple prompt
      const pageId = prompt("Enter the ID of the page to paste to:");
      if (pageId) {
        this.pasteBlockToChosenPage(clipboardId, pageId);
      }
    }
  }

  /**
   * Paste a block to a chosen page
   * @param {string} clipboardId - The clipboard item ID
   * @param {string} pageId - The page ID to paste to
   */
  pasteBlockToChosenPage(clipboardId, pageId) {
    console.log(
      "🔍 Block Exchange: Pasting clipboard item to page",
      clipboardId,
      pageId
    );

    // Get the CSRF token
    const csrfToken = document.querySelector(
      "input[name='csrfmiddlewaretoken']"
    ).value;

    // Show a loading notification
    notify.info("Pasting block to page...");

    // Make the API request to paste the block
    pasteBlockToPage(clipboardId, pageId, csrfToken)
      .then((data) => {
        if (data.success) {
          // Show success notification
          notify.success("Block pasted successfully");

          // Create a nice action link to edit the page
          const editUrl = `/admin/pages/${pageId}/edit/?clipboard_paste_pending=true`;
          notify.success(
            "Block pasted successfully",
            "success",
            "Edit Page",
            editUrl
          );

          // Optionally, redirect to the page
          if (
            confirm(
              "Block pasted successfully. Would you like to edit the page now?"
            )
          ) {
            window.location.href = editUrl;
          }
        } else {
          // Show error notification
          notify.error(
            "Failed to paste block: " + (data.error || "Unknown error")
          );
        }
      })
      .catch((error) => {
        // Show error notification
        notify.error("Error: " + error.message);
      });
  }
}

// Create and initialize the clipboard page handler
const clipboardPage = new ClipboardPage();

// Initialize when DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  clipboardPage.initialize();
});

export { clipboardPage };
