/**
 * Wagtail Block Exchange - JavaScript module
 *
 * This script adds the ability to copy blocks between pages in the Wagtail admin.
 */

(function () {
  "use strict";

  // Main initialization function with error handling
  function initBlockExchange() {
    try {
      console.log("Block Exchange: Initializing...");
      // Set up CSRF protection for AJAX requests
      const csrfToken = document.querySelector(
        'input[name="csrfmiddlewaretoken"]'
      )?.value;
      console.log("Block Exchange: CSRF token found:", !!csrfToken);

      if (isPageEditor()) {
        console.log(
          "Block Exchange: Detected page editor, setting up copy buttons"
        );
        // Execute immediately, don't wait for timeout
        setupCopyButtons();

        // DISABLED: Setup block insertion dialog - this has been moved to inline JS in wagtail_hooks.py
        // setupBlockInsertionDialog();
        console.log(
          "Block Exchange: Skipping setupBlockInsertionDialog (moved to hooks)"
        );
      }

      if (isClipboardPage()) {
        console.log("Block Exchange: Detected clipboard page");
        initClipboardPage();
      }
    } catch (err) {
      console.error("Block Exchange: Error during initialization:", err);
    }
  }

  // Setup the copy buttons for all blocks
  function setupCopyButtons() {
    try {
      console.log("Block Exchange: Setting up copy buttons immediately");
      // Execute immediately instead of waiting
      addCopyButtonsToBlocks();
      setupMutationObserver();
    } catch (err) {
      console.error("Block Exchange: Error setting up copy buttons:", err);
    }
  }

  // Add copy buttons to all blocks in the page
  function addCopyButtonsToBlocks() {
    try {
      // Target controls using multiple selectors for future-proofing
      // First try data attributes (most stable), then fall back to class-based selectors
      const controlsSelectors = [
        "[data-panel-controls]", // Primary: data attribute
        ".w-panel__controls", // Secondary: current class name
        ".stream-controls", // Fallback: older Wagtail versions
        ".block-controls", // Fallback: generic name
      ];

      // Combine all selectors
      const combinedSelector = controlsSelectors.join(", ");
      console.log(
        "Block Exchange: Looking for controls using selector:",
        combinedSelector
      );

      // Debug all available control elements
      const allControls = document.querySelectorAll(combinedSelector);
      console.log(
        `Block Exchange: Found ${allControls.length} control elements:`,
        allControls
      );

      // Try a more generic approach if no controls found
      if (allControls.length === 0) {
        console.log(
          "Block Exchange: No controls found with standard selectors, trying alternate approach"
        );
        // Look for any buttons that might be duplicate buttons
        const possibleDuplicateButtons = document.querySelectorAll(
          'button[title="Duplicate"], .duplicate, [data-streamfield-action="DUPLICATE"]'
        );
        console.log(
          `Block Exchange: Found ${possibleDuplicateButtons.length} possible duplicate buttons`
        );

        possibleDuplicateButtons.forEach((button) => {
          const controlsContainer = button.parentElement;
          if (controlsContainer) {
            console.log(
              "Block Exchange: Found potential controls container from duplicate button:",
              controlsContainer
            );
            addCopyButtonToControls(controlsContainer);
          }
        });

        return;
      }

      // Find all control containers
      document
        .querySelectorAll(combinedSelector)
        .forEach(function (controlsContainer) {
          console.log(
            "Block Exchange: Processing control container:",
            controlsContainer
          );
          // Add our copy button if it doesn't already exist
          if (!controlsContainer.querySelector(".copy-to-clipboard-button")) {
            addCopyButtonToControls(controlsContainer);
          } else {
            console.log(
              "Block Exchange: Copy button already exists for this container"
            );
          }
        });
    } catch (err) {
      console.error(
        "Block Exchange: Error adding copy buttons to blocks:",
        err
      );
    }
  }

  // Attach a mutation observer to detect dynamically added blocks
  function setupMutationObserver() {
    try {
      // Try to target the most reliable container for the observer
      const contentContainer =
        document.querySelector(".content") ||
        document.querySelector("main") ||
        document.body;

      console.log(
        "Block Exchange: Setting up mutation observer on:",
        contentContainer
      );

      if (!contentContainer) {
        console.warn(
          "Block Exchange: No suitable container found for mutation observer"
        );
        return;
      }

      const observer = new MutationObserver(function (mutations) {
        mutations.forEach(function (mutation) {
          // Look for added nodes that might contain blocks
          mutation.addedNodes.forEach(function (node) {
            if (node.nodeType === Node.ELEMENT_NODE) {
              // Check if this node is or contains control panels
              if (
                node.matches &&
                node.matches("[data-panel-controls], .w-panel__controls")
              ) {
                console.log(
                  "Block Exchange: Mutation detected new control panel:",
                  node
                );
                addCopyButtonToControls(node);
              }

              // Also check children
              const controls = node.querySelectorAll(
                "[data-panel-controls], .w-panel__controls"
              );
              if (controls.length > 0) {
                console.log(
                  `Block Exchange: Mutation detected ${controls.length} controls in new node`
                );
                controls.forEach(addCopyButtonToControls);
              }
            }
          });
        });
      });

      observer.observe(contentContainer, { childList: true, subtree: true });
      console.log("Block Exchange: Mutation observer successfully attached");
    } catch (err) {
      console.error("Block Exchange: Error setting up mutation observer:", err);
    }
  }

  // Add a copy button to a block's controls container
  function addCopyButtonToControls(controlsContainer) {
    try {
      console.log(
        "Block Exchange: Adding copy button to control container:",
        controlsContainer
      );

      // Check if we've already added a button to this container
      if (controlsContainer.querySelector(".copy-to-clipboard-button")) {
        console.log("Block Exchange: Skipping - button already exists");
        return;
      }

      // Find the duplicate button by data attribute first, then fallback to other attributes
      const duplicateButton =
        controlsContainer.querySelector(
          '[data-streamfield-action="DUPLICATE"]'
        ) ||
        controlsContainer.querySelector('[title="Duplicate"]') ||
        controlsContainer.querySelector(".duplicate");

      if (!duplicateButton) {
        console.warn(
          "Block Exchange: No duplicate button found in controls container"
        );
        return;
      }

      console.log("Block Exchange: Found duplicate button:", duplicateButton);
      console.log(
        "Block Exchange: Duplicate button classes:",
        duplicateButton.className
      );

      // Create our copy button matching the style of existing buttons
      const copyButton = document.createElement("button");
      copyButton.type = "button";
      copyButton.className = "copy-to-clipboard-button";
      copyButton.title = "Copy to Clipboard";
      copyButton.setAttribute("aria-label", "Copy to Clipboard");
      copyButton.setAttribute("data-streamfield-action", "COPY_TO_CLIPBOARD");

      console.log(
        "Block Exchange: Created copy button with initial class:",
        copyButton.className
      );

      // Copy classes from the duplicate button for consistent styling
      const duplicateClasses = duplicateButton.className.split(" ");
      console.log(
        "Block Exchange: Duplicate button classes:",
        duplicateClasses
      );

      duplicateClasses.forEach(function (cls) {
        if (
          cls !== "duplicate" &&
          !cls.includes("duplicate") &&
          !cls.includes("move") &&
          !cls.includes("delete")
        ) {
          copyButton.classList.add(cls);
          console.log(`Block Exchange: Added class "${cls}" to copy button`);
        } else {
          console.log(`Block Exchange: Skipped class "${cls}"`);
        }
      });

      // Apply base button classes from Wagtail that we've seen in the HTML
      const wagtailButtonClasses = [
        "button",
        "button--icon",
        "text-replace",
        "white",
      ];

      wagtailButtonClasses.forEach((cls) => {
        // Only add if the duplicate button has this class
        if (duplicateButton.classList.contains(cls)) {
          copyButton.classList.add(cls);
          console.log(
            `Block Exchange: Added Wagtail button class "${cls}" to copy button`
          );
        } else {
          console.log(
            `Block Exchange: Duplicate button doesn't have class "${cls}"`
          );
        }
      });

      console.log(
        "Block Exchange: Copy button final classes:",
        copyButton.className
      );

      // Create the icon with direct CSS instead of relying on Wagtail's icon system
      // This will make a small clipboard icon using CSS
      copyButton.innerHTML =
        '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path></svg>';
      console.log("Block Exchange: Added inline SVG clipboard icon");

      // Insert after the duplicate button
      duplicateButton.insertAdjacentElement("afterend", copyButton);
      console.log(
        "Block Exchange: Button inserted into DOM after duplicate button"
      );

      // Log the HTML structure after insertion
      console.log(
        "Block Exchange: Button HTML structure:",
        copyButton.outerHTML
      );
      console.log(
        "Block Exchange: Parent container HTML:",
        controlsContainer.outerHTML
      );

      // Set up the click handler
      copyButton.addEventListener("click", handleCopyButtonClick);
      console.log("Block Exchange: Click handler attached to button");
    } catch (err) {
      console.error(
        "Block Exchange: Error adding copy button to controls:",
        err
      );
    }
  }

  // Handle clicks on the copy button
  function handleCopyButtonClick(e) {
    try {
      e.preventDefault();
      e.stopPropagation();
      console.log("Block Exchange: Copy button clicked");

      // Find the parent block element
      const button = e.currentTarget;
      const blockElement = findParentBlock(button);

      if (!blockElement) {
        console.error("Block Exchange: Could not find parent block element");
        return;
      }

      console.log("Block Exchange: Found parent block:", blockElement);

      // Get block ID and page ID
      const blockId = getBlockId(blockElement);
      const pageId = getPageId();

      console.log("Block Exchange: Block ID:", blockId);
      console.log("Block Exchange: Page ID:", pageId);

      if (!blockId || !pageId) {
        console.error(
          "Block Exchange: Could not determine block ID or page ID"
        );
        return;
      }

      // Copy the block to the clipboard without asking for a label
      copyBlockToClipboard(pageId, blockId, "");
    } catch (err) {
      console.error("Block Exchange: Error handling copy button click:", err);
    }
  }

  // Find the parent block element from a button
  function findParentBlock(element) {
    try {
      console.log("Block Exchange: Finding parent block for element:", element);
      // Look for various selectors that might identify a block
      const selectors = [
        ".stream-field__block",
        "[data-contentpath]",
        '[id^="block-"]',
        "[data-block-id]",
        ".w-panel",
      ];

      // Navigate up to find the block container
      let current = element;
      while (current && current !== document.body) {
        // Check if the current element matches any of our selectors
        for (const selector of selectors) {
          if (current.matches && current.matches(selector)) {
            console.log(
              `Block Exchange: Found parent block with selector "${selector}":`,
              current
            );
            return current;
          }
        }
        current = current.parentElement;
      }
      console.warn("Block Exchange: Could not find a matching parent block");
      return null;
    } catch (err) {
      console.error("Block Exchange: Error finding parent block:", err);
      return null;
    }
  }

  // Get the block ID from a block element
  function getBlockId(blockElement) {
    try {
      console.log(
        "Block Exchange: Getting block ID from element:",
        blockElement
      );
      // Try multiple possible attributes where the ID might be stored
      const id =
        blockElement.dataset.contentpath ||
        blockElement.dataset.id ||
        blockElement.dataset.blockId ||
        blockElement.id ||
        blockElement.querySelector("[data-contentpath]")?.dataset.contentpath ||
        blockElement.querySelector("[data-block-id]")?.dataset.blockId ||
        blockElement.querySelector('[id^="block-"]')?.id;

      console.log("Block Exchange: Retrieved block ID:", id);
      return id;
    } catch (err) {
      console.error("Block Exchange: Error getting block ID:", err);
      return null;
    }
  }

  // Send an AJAX request to copy a block to the clipboard
  function copyBlockToClipboard(pageId, blockId, label) {
    try {
      console.log("Block Exchange: Copying block to clipboard", {
        pageId: pageId,
        blockId: blockId,
        label: label,
      });

      // Create the form data
      const formData = new FormData();
      formData.append("page_id", pageId);
      formData.append("block_id", blockId);
      if (label) formData.append("label", label);

      // Get the CSRF token from the page
      const csrfToken = document.querySelector(
        'input[name="csrfmiddlewaretoken"]'
      ).value;

      console.log(
        "Block Exchange: Preparing AJAX request with CSRF token:",
        !!csrfToken
      );

      // Send the request
      fetch("/admin/block-exchange/copy/", {
        method: "POST",
        headers: {
          "X-CSRFToken": csrfToken,
        },
        body: formData,
      })
        .then((response) => {
          console.log(
            "Block Exchange: Server response status:",
            response.status
          );
          return response.json();
        })
        .then((data) => {
          console.log("Block Exchange: Server response data:", data);
          if (data.success) {
            // Add action to view clipboard
            const message = "Block copied to clipboard";
            const actionText = "View clipboard";
            const actionUrl = "/admin/block-exchange/clipboard/";
            showNotification(message, "success", actionText, actionUrl);

            // Log notification system availability for debugging
            console.log(
              "Block Exchange: Native Wagtail notify available:",
              !!(window.wagtail && typeof window.wagtail.notify === "object")
            );
            console.log(
              "Block Exchange: Wagtail messages API available:",
              !!(window.wagtail && typeof window.wagtail.messages === "object")
            );
          } else {
            showNotification(
              "Failed to copy block: " + (data.error || "Unknown error"),
              "error"
            );
          }
        })
        .catch((error) => {
          console.error("Block Exchange: Error during AJAX request:", error);
          showNotification("Error copying block: " + error, "error");
        });
    } catch (err) {
      console.error("Block Exchange: Error in copy block function:", err);
    }
  }

  // Initialize the clipboard page
  function initClipboardPage() {
    try {
      console.log("Block Exchange: Initializing clipboard page");
      document.addEventListener("DOMContentLoaded", function () {
        console.log("Block Exchange: DOM loaded for clipboard page");
        // Set up paste buttons
        document
          .querySelectorAll(".paste-block-button")
          .forEach(function (button) {
            button.addEventListener("click", handlePasteButtonClick);
          });

        // Set up delete buttons
        document
          .querySelectorAll(".delete-clipboard-item-button")
          .forEach(function (button) {
            button.addEventListener("click", handleDeleteButtonClick);
          });
      });
    } catch (err) {
      console.error("Block Exchange: Error initializing clipboard page:", err);
    }
  }

  // Handle clicks on the paste button in the clipboard view
  function handlePasteButtonClick(e) {
    e.preventDefault();
    console.log("Block Exchange: Paste button clicked");

    // Get the clipboard item ID
    const clipboardId = e.currentTarget.dataset.clipboardId;
    console.log("Block Exchange: Clipboard ID:", clipboardId);

    // Open page chooser dialog
    openPageChooserForPaste(clipboardId);
  }

  // Open a page chooser dialog to select the destination page
  function openPageChooserForPaste(clipboardId) {
    try {
      console.log(
        "Block Exchange: Opening page chooser for clipboard item:",
        clipboardId
      );

      // Try to find the admin page chooser URL (most reliable method)
      const adminChooserUrl = "/admin/choose-page/";

      // Use Wagtail's built-in modal system
      if (typeof window.ModalWorkflow === "function") {
        console.log("Block Exchange: Using ModalWorkflow to open page chooser");

        // Create the modal with proper configuration
        const modal = window.ModalWorkflow({
          url: adminChooserUrl,
          onload: {
            // We only need to handle the final "chosen" event
            chosen: function (modal, responseData) {
              console.log("Block Exchange: Page chosen:", responseData);
              if (responseData && responseData.id) {
                modal.close();
                pasteBlockToPage(clipboardId, responseData.id);
              }
            },
          },
        });

        // Add event delegation to handle navigation links
        // We need to wait for the modal to be in the DOM
        setTimeout(() => {
          // Find the modal dialog element
          const modalElement = document.querySelector(".modal");
          if (!modalElement) {
            console.warn(
              "Block Exchange: Could not find modal element for event delegation"
            );
            return;
          }

          // Add click handler for navigation links
          modalElement.addEventListener("click", function (e) {
            // Look for navigation links
            if (
              e.target &&
              (e.target.classList.contains("navigate-pages") ||
                e.target.closest("a.navigate-pages"))
            ) {
              e.preventDefault(); // Prevent the default link behavior

              // Find the actual link element (could be the target or a parent)
              const link = e.target.classList.contains("navigate-pages")
                ? e.target
                : e.target.closest("a.navigate-pages");

              console.log(
                "Block Exchange: Intercepted navigation click:",
                link.href
              );

              // Use the modal's loadUrl method to handle navigation properly
              modal.loadUrl(link.href);
            }

            // Also handle the choose page links (when a user selects a page)
            if (
              e.target &&
              (e.target.classList.contains("choose-page") ||
                e.target.closest("a.choose-page"))
            ) {
              e.preventDefault(); // Prevent the default link behavior

              // Find the actual link element (could be the target or a parent)
              const link = e.target.classList.contains("choose-page")
                ? e.target
                : e.target.closest("a.choose-page");

              console.log("Block Exchange: Page selected via link:", link.href);
              console.log("Block Exchange: Link element:", link);
              console.log("Block Exchange: Link dataset:", link.dataset);

              // Try multiple patterns to extract page ID based on different Wagtail versions
              let pageId = null;

              // Check for data attributes first (most reliable)
              if (link.dataset && link.dataset.id) {
                pageId = link.dataset.id;
                console.log(
                  "Block Exchange: Found page ID in data-id attribute:",
                  pageId
                );
              }
              // If there's a data-page-id attribute
              else if (link.dataset && link.dataset.pageId) {
                pageId = link.dataset.pageId;
                console.log(
                  "Block Exchange: Found page ID in data-page-id attribute:",
                  pageId
                );
              }
              // Try to extract from URL
              else {
                // Try several URL patterns - Wagtail has changed these over time
                const patterns = [
                  /\/choose-page\/(\d+)\/select\//, // Standard format
                  /\/choose-page\/(\d+)\//, // Alternate format
                  /\#(\d+)$/, // Hashtag format (like #108)
                  /\/pages\/(\d+)\//, // Direct page URL format
                ];

                for (const pattern of patterns) {
                  const match = link.href.match(pattern);
                  if (match && match[1]) {
                    pageId = match[1];
                    console.log(
                      `Block Exchange: Extracted page ID using pattern ${pattern}:`,
                      pageId
                    );
                    break;
                  }
                }
              }

              // If we have a page ID, proceed with pasting
              if (pageId) {
                console.log("Block Exchange: Using page ID for paste:", pageId);

                // Close the modal and paste to the selected page
                modal.close();
                pasteBlockToPage(clipboardId, pageId);
              } else {
                console.error(
                  "Block Exchange: Could not extract page ID from link:",
                  link.href
                );

                // Try a last resort - look for text content that might contain the page ID
                const pageIdText = link.innerText.match(/ID: (\d+)/);
                if (pageIdText && pageIdText[1]) {
                  pageId = pageIdText[1];
                  console.log(
                    "Block Exchange: Extracted page ID from text:",
                    pageId
                  );
                  modal.close();
                  pasteBlockToPage(clipboardId, pageId);
                } else {
                  showNotification(
                    "Could not determine page ID. Please try a different page.",
                    "error"
                  );
                }
              }
            }
          });

          console.log(
            "Block Exchange: Added event delegation for modal navigation"
          );
        }, 100); // Short delay to ensure modal is in DOM

        return;
      }

      // Modern Wagtail API fallback (4.x+)
      if (
        window.wagtail &&
        typeof window.wagtail.choosers === "object" &&
        typeof window.wagtail.choosers.pageChooser === "function"
      ) {
        console.log(
          "Block Exchange: Using modern wagtail.choosers.pageChooser API"
        );
        window.wagtail.choosers.pageChooser().then(function (response) {
          console.log("Block Exchange: Page chosen via modern API:", response);
          if (response && response.id) {
            pasteBlockToPage(clipboardId, response.id);
          }
        });
        return;
      }

      // Last resort - if nothing else works, use a prompt
      console.warn(
        "Block Exchange: No modal system available, using prompt fallback"
      );
      const pageId = prompt("Enter the ID of the page to paste to:");
      if (pageId && !isNaN(parseInt(pageId, 10))) {
        pasteBlockToPage(clipboardId, pageId);
      }
    } catch (err) {
      console.error("Block Exchange: Error opening page chooser:", err);
      showNotification("Error opening page chooser: " + err.message, "error");

      // Ultimate fallback - prompt in case of any errors
      try {
        const pageId = prompt("Enter the ID of the page to paste to:");
        if (pageId && !isNaN(parseInt(pageId, 10))) {
          pasteBlockToPage(clipboardId, pageId);
        }
      } catch (e) {
        console.error("Block Exchange: Even the prompt fallback failed:", e);
      }
    }
  }

  // Handle deleting an item from the clipboard
  function handleDeleteButtonClick(e) {
    e.preventDefault();
    console.log("Block Exchange: Delete button clicked");

    // Get the clipboard item ID
    const clipboardId = e.currentTarget.dataset.clipboardId;
    console.log("Block Exchange: Clipboard ID to delete:", clipboardId);

    // Confirm deletion
    if (
      !confirm("Are you sure you want to remove this item from your clipboard?")
    ) {
      console.log("Block Exchange: User cancelled deletion");
      return;
    }

    // Delete the item
    deleteClipboardItem(clipboardId);
  }

  // Send an AJAX request to delete a clipboard item
  function deleteClipboardItem(clipboardId) {
    console.log("Block Exchange: Deleting clipboard item:", clipboardId);
    // Get the CSRF token from the page
    const csrfToken = document.querySelector(
      'input[name="csrfmiddlewaretoken"]'
    ).value;

    // Send the request
    fetch(`/admin/block-exchange/clipboard/clear/${clipboardId}/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Block Exchange: Delete response:", data);
        if (data.success) {
          // Remove the item from the DOM
          const item = document.querySelector(
            `.clipboard-item[data-clipboard-id="${clipboardId}"]`
          );
          if (item) item.remove();

          showNotification("Item removed from clipboard", "success");
        } else {
          showNotification(
            "Failed to remove item: " + (data.error || "Unknown error"),
            "error"
          );
        }
      })
      .catch((error) => {
        console.error("Block Exchange: Error deleting item:", error);
        showNotification("Error removing item: " + error, "error");
      });
  }

  // Send an AJAX request to paste a block to a page
  function pasteBlockToPage(clipboardId, pageId, fieldName, position) {
    console.log("Block Exchange: Pasting block", {
      clipboardId: clipboardId,
      pageId: pageId,
      fieldName: fieldName,
      position: position,
    });

    // Create the form data
    const formData = new FormData();
    formData.append("clipboard_id", clipboardId);
    formData.append("page_id", pageId);
    if (fieldName) formData.append("field_name", fieldName);
    if (position) formData.append("position", position);

    // Get the CSRF token from the page
    const csrfToken = document.querySelector(
      'input[name="csrfmiddlewaretoken"]'
    ).value;

    // Send the request
    fetch("/admin/block-exchange/paste/", {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
      },
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Block Exchange: Paste response:", data);
        if (data.success) {
          // Create success message with a link to edit the page
          const message = "Block pasted successfully";
          const actionText = "Edit page";
          const actionUrl = `/admin/pages/${pageId}/edit/`;

          // Use Wagtail's notification system with an action link
          showNotification(message, "success", actionText, actionUrl);
        } else {
          showNotification(
            "Failed to paste block: " + (data.error || "Unknown error"),
            "error"
          );
        }
      })
      .catch((error) => {
        console.error("Block Exchange: Error pasting block:", error);
        showNotification("Error pasting block: " + error, "error");
      });
  }

  // Helper function to show a notification
  function showNotification(text, type, actionText, actionUrl) {
    try {
      console.log(`Block Exchange: Showing notification (${type}):`, text);

      // Detect which notification systems are available
      const hasNotify = !!(
        window.wagtail && typeof window.wagtail.notify === "object"
      );
      const hasMessages = !!(
        window.wagtail &&
        typeof window.wagtail.messages === "object" &&
        typeof window.wagtail.messages.add === "function"
      );
      console.log("Block Exchange: Notification systems available:", {
        hasNotify,
        hasMessages,
      });

      // First try the modern Wagtail notification API
      if (hasNotify) {
        try {
          // Try object format first (modern Wagtail)
          if (actionText && actionUrl) {
            window.wagtail.notify[type || "info"]({
              message: text,
              actionText: actionText,
              actionUrl: actionUrl,
            });
            console.log("Block Exchange: Used notify with object format");
            return;
          } else {
            // String format for simple notifications
            window.wagtail.notify[type || "info"](text);
            console.log("Block Exchange: Used notify with string format");
            return;
          }
        } catch (err) {
          console.warn("Block Exchange: Wagtail notify API failed:", err);
        }
      }

      // Fall back to Django messages API if available
      if (hasMessages) {
        let message = text;
        if (actionText && actionUrl) {
          // Add link to the message text
          message += ` <a href="${actionUrl}" class="button">${actionText}</a>`;
        }

        try {
          window.wagtail.messages.add(message, type || "info");
          console.log("Block Exchange: Used messages.add");
          return;
        } catch (err) {
          console.warn("Block Exchange: messages.add failed:", err);
        }
      }

      // Create our own notification element if all else fails
      console.log("Block Exchange: Creating custom DOM notification");
      createCustomNotification(text, type, actionText, actionUrl);
    } catch (err) {
      console.error("Block Exchange: Critical error in showNotification:", err);
      // Even if everything fails, still try to show a custom notification
      createCustomNotification(text, type || "info", actionText, actionUrl);
    }
  }

  // Create a custom notification directly in the DOM with inline styles
  function createCustomNotification(text, type, actionText, actionUrl) {
    try {
      // Convert type to standardized value
      const normalizedType = (type || "info").toLowerCase();

      // Map types to colors
      const colors = {
        success: "#1d933b",
        error: "#cd3238",
        warning: "#e9b04d",
        info: "#262626",
      };

      const backgroundColor = colors[normalizedType] || colors.info;

      // Check if we already have a notification container
      let container = document.querySelector(".block-exchange-notifications");

      if (!container) {
        // Create container with fixed positioning at the top of the page
        container = document.createElement("div");
        container.className = "block-exchange-notifications";
        container.setAttribute(
          "style",
          `
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          z-index: 9999;
          font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
        `
        );
        document.body.appendChild(container);
      }

      // Create notification element
      const notification = document.createElement("div");
      notification.setAttribute(
        "style",
        `
        position: relative;
        padding: 15px 40px 15px 20px;
        background-color: ${backgroundColor};
        color: white;
        margin-bottom: 1px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
      `
      );

      // Create message element
      const message = document.createElement("div");
      message.innerHTML = text;
      message.setAttribute(
        "style",
        `
        flex: 1;
        font-size: 14px;
      `
      );

      notification.appendChild(message);

      // Add action link if provided
      if (actionText && actionUrl) {
        const action = document.createElement("a");
        action.href = actionUrl;
        action.textContent = actionText;
        action.setAttribute(
          "style",
          `
          margin-left: 15px;
          color: white;
          text-decoration: underline;
          font-weight: bold;
          white-space: nowrap;
        `
        );
        notification.appendChild(action);
      }

      // Add close button
      const closeBtn = document.createElement("button");
      closeBtn.innerHTML = "×";
      closeBtn.setAttribute(
        "style",
        `
        position: absolute;
        right: 15px;
        top: 50%;
        transform: translateY(-50%);
        color: white;
        border: none;
        background: transparent;
        cursor: pointer;
        font-size: 20px;
        line-height: 1;
        padding: 0;
        width: 20px;
        height: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
      `
      );

      closeBtn.addEventListener("click", () => {
        notification.remove();
      });

      notification.appendChild(closeBtn);

      // Add to container
      container.appendChild(notification);

      // Auto-remove after 5 seconds
      setTimeout(() => {
        if (notification.parentNode) {
          notification.remove();
        }
      }, 5000);

      console.log(
        "Block Exchange: Custom notification created and added to DOM"
      );
    } catch (err) {
      console.error(
        "Block Exchange: Failed to create custom notification:",
        err
      );
    }
  }

  // Helper function to get the page ID
  function getPageId() {
    try {
      console.log("Block Exchange: Getting page ID");
      // Try to get it from the URL first
      const match = window.location.pathname.match(
        /\/admin\/pages\/(\d+)\/edit/
      );
      if (match) {
        console.log("Block Exchange: Found page ID in URL:", match[1]);
        return match[1];
      }

      // Try to get it from the form
      const pageIdInput = document.querySelector('input[name="page_id"]');
      if (pageIdInput) {
        console.log(
          "Block Exchange: Found page ID in form:",
          pageIdInput.value
        );
        return pageIdInput.value;
      }

      // Try to get it from the body data attribute
      const body = document.body;
      if (body.dataset.pageId) {
        console.log(
          "Block Exchange: Found page ID in body dataset:",
          body.dataset.pageId
        );
        return body.dataset.pageId;
      }

      console.warn("Block Exchange: Could not find page ID");
      return null;
    } catch (err) {
      console.error("Block Exchange: Error getting page ID:", err);
      return null;
    }
  }

  // Check if current page is the page editor
  function isPageEditor() {
    try {
      const isEditor =
        window.location.pathname.includes("/admin/pages/") &&
        window.location.pathname.includes("/edit/");
      console.log("Block Exchange: Is page editor?", isEditor);
      return isEditor;
    } catch (err) {
      console.error("Block Exchange: Error checking if page editor:", err);
      return false;
    }
  }

  // Check if current page is the clipboard page
  function isClipboardPage() {
    try {
      const isClipboard = window.location.pathname.includes(
        "/admin/block-exchange/clipboard/"
      );
      console.log("Block Exchange: Is clipboard page?", isClipboard);
      return isClipboard;
    } catch (err) {
      console.error("Block Exchange: Error checking if clipboard page:", err);
      return false;
    }
  }

  // Setup the block insertion dialog to include clipboard items
  function setupBlockInsertionDialog() {
    // DISABLED: This functionality has been moved to inline JS in wagtail_hooks.py
    console.log(
      "Block Exchange: setupBlockInsertionDialog DISABLED - functionality moved to hooks"
    );
    return; // Early return to prevent duplicate clipboard sections

    try {
      console.log(
        "Block Exchange: Setting up block insertion dialog enhancement"
      );

      // Use a mutation observer to detect when the insert block dialog appears
      const bodyObserver = new MutationObserver(function (mutations) {
        mutations.forEach(function (mutation) {
          mutation.addedNodes.forEach(function (node) {
            if (node.nodeType === Node.ELEMENT_NODE) {
              // Look for the insert block dialog
              if (
                node.querySelector &&
                (node.classList.contains("insert-block") ||
                  node.querySelector(".insert-block") ||
                  node.querySelector("[data-streamfield-stream-container]"))
              ) {
                console.log("Block Exchange: Detected insert block dialog");
                enhanceInsertBlockDialog(node);
              }
            }
          });
        });
      });

      // Start observing the body for the dialog
      bodyObserver.observe(document.body, { childList: true, subtree: true });
      console.log("Block Exchange: Body observer for insert dialog attached");
    } catch (err) {
      console.error(
        "Block Exchange: Error setting up block insertion dialog:",
        err
      );
    }
  }

  // Enhance the insert block dialog with clipboard items
  function enhanceInsertBlockDialog(dialogNode) {
    // DISABLED: This functionality has been moved to inline JS in wagtail_hooks.py
    console.log(
      "Block Exchange: enhanceInsertBlockDialog DISABLED - moved to hooks"
    );
    return; // Early return to prevent duplicate clipboard sections

    try {
      console.log("Block Exchange: Enhancing insert block dialog");

      // Find the actual dialog container
      const dialog = dialogNode.classList.contains("insert-block")
        ? dialogNode
        : dialogNode.querySelector(".insert-block") ||
          dialogNode.closest(".insert-block") ||
          dialogNode.querySelector("[data-streamfield-stream-container]") ||
          dialogNode.classList.contains("block-chooser")
        ? dialogNode
        : dialogNode.querySelector(".block-chooser") || dialogNode;

      console.log("Block Exchange: Found dialog container:", dialog);

      // Check if we've already enhanced this dialog
      if (dialog.querySelector(".clipboard-items-section")) {
        console.log("Block Exchange: Dialog already enhanced");
        return;
      }

      // Fetch clipboard items
      fetchClipboardItems()
        .then((items) => {
          if (!items || items.length === 0) {
            console.log("Block Exchange: No clipboard items to display");
            return;
          }

          console.log(
            "Block Exchange: Adding clipboard items to dialog:",
            items
          );

          // Create a section for clipboard items
          const clipboardSection = document.createElement("div");
          clipboardSection.className = "clipboard-items-section";
          clipboardSection.setAttribute(
            "style",
            "margin-top: 20px; border-top: 1px solid #eee; padding-top: 10px;"
          );

          // Add heading
          const heading = document.createElement("h3");
          heading.textContent = "Clipboard Items";
          heading.setAttribute(
            "style",
            "font-size: 1.1em; font-weight: bold; margin-bottom: 10px;"
          );
          clipboardSection.appendChild(heading);

          // Create grid for items (matching Wagtail's layout)
          const itemsGrid = document.createElement("div");
          itemsGrid.setAttribute(
            "style",
            "display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 10px;"
          );
          clipboardSection.appendChild(itemsGrid);

          // Add each clipboard item
          items.forEach((item) => {
            const itemEl = createClipboardItemElement(item, dialog);
            itemsGrid.appendChild(itemEl);
          });

          // Find the right place to insert our section
          // Try multiple potential insertion points
          let inserted = false;

          // First try: after the search box
          const searchBox = dialog.querySelector(
            'input[type="text"], input[placeholder*="Search"]'
          );
          if (searchBox) {
            // Try direct parent first, then walk up to find a suitable container
            let container = searchBox.closest("div");
            let maxDepth = 3; // Limit how far up we'll look

            while (container && maxDepth > 0) {
              // Try inserting after this container
              try {
                container.parentNode.insertBefore(
                  clipboardSection,
                  container.nextSibling
                );
                console.log("Block Exchange: Inserted after search container");
                inserted = true;
                break;
              } catch (err) {
                // Try the parent
                container = container.parentNode;
                maxDepth--;
              }
            }
          }

          // Second try: before the groups of blocks
          if (!inserted) {
            const blockGroups = dialog.querySelector(
              ".block-types-grouped, .sorted-blocks, .fields, .block-types-list"
            );
            if (blockGroups) {
              blockGroups.parentNode.insertBefore(
                clipboardSection,
                blockGroups
              );
              console.log("Block Exchange: Inserted before block groups");
              inserted = true;
            }
          }

          // Third try: at the beginning or end of the dialog
          if (!inserted) {
            // Try beginning first
            if (dialog.firstChild) {
              dialog.insertBefore(clipboardSection, dialog.firstChild);
              console.log("Block Exchange: Inserted at beginning of dialog");
            } else {
              // Append at the end as last resort
              dialog.appendChild(clipboardSection);
              console.log("Block Exchange: Appended to dialog");
            }
          }

          console.log("Block Exchange: Clipboard items added to dialog");
        })
        .catch((err) => {
          console.error("Block Exchange: Error fetching clipboard items:", err);
        });
    } catch (err) {
      console.error(
        "Block Exchange: Error enhancing insert block dialog:",
        err
      );
    }
  }

  // Create an element for a clipboard item
  function createClipboardItemElement(item, dialogContainer) {
    const itemEl = document.createElement("div");

    // Apply styling similar to other block options in the dialog
    itemEl.setAttribute(
      "style",
      `
      position: relative;
      background-color: #fff;
      border: 1px solid #e6e6e6;
      border-radius: 3px;
      padding: 10px;
      cursor: pointer;
      transition: border-color 0.2s, box-shadow 0.2s;
    `
    );

    // Add hover effects
    itemEl.addEventListener("mouseover", () => {
      itemEl.style.borderColor = "#007d7e";
      itemEl.style.boxShadow = "0 2px 4px rgba(0,0,0,0.1)";
    });

    itemEl.addEventListener("mouseout", () => {
      itemEl.style.borderColor = "#e6e6e6";
      itemEl.style.boxShadow = "none";
    });

    // Title
    const title = document.createElement("div");
    title.textContent =
      item.label || item.block_type_display || item.block_type;
    title.setAttribute(
      "style",
      "font-weight: bold; margin-bottom: 5px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;"
    );
    itemEl.appendChild(title);

    // Type label
    const type = document.createElement("div");
    type.textContent = item.block_type_display || item.block_type;
    type.setAttribute(
      "style",
      "font-size: 0.8em; color: #666; margin-bottom: 5px;"
    );
    itemEl.appendChild(type);

    // Add delete button
    const deleteBtn = document.createElement("button");
    deleteBtn.innerHTML = "×";
    deleteBtn.setAttribute(
      "style",
      `
      position: absolute;
      top: 5px;
      right: 5px;
      width: 18px;
      height: 18px;
      border-radius: 50%;
      background-color: #f5f5f5;
      border: 1px solid #ddd;
      color: #666;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 14px;
      line-height: 1;
      padding: 0;
      cursor: pointer;
      opacity: 0.7;
      transition: opacity 0.2s, background-color 0.2s;
    `
    );

    deleteBtn.addEventListener("mouseover", (e) => {
      e.stopPropagation(); // Prevent triggering the parent's hover
      deleteBtn.style.backgroundColor = "#ff5c5c";
      deleteBtn.style.borderColor = "#ff4040";
      deleteBtn.style.color = "white";
      deleteBtn.style.opacity = "1";
    });

    deleteBtn.addEventListener("mouseout", (e) => {
      e.stopPropagation(); // Prevent triggering the parent's hover
      deleteBtn.style.backgroundColor = "#f5f5f5";
      deleteBtn.style.borderColor = "#ddd";
      deleteBtn.style.color = "#666";
      deleteBtn.style.opacity = "0.7";
    });

    // Handle delete click
    deleteBtn.addEventListener("click", (e) => {
      e.stopPropagation(); // Don't trigger the parent click
      if (confirm(`Remove "${title.textContent}" from clipboard?`)) {
        deleteClipboardItem(item.id).then(() => {
          // Remove this element from the DOM
          itemEl.remove();

          // Check if there are any items left
          const itemsGrid = dialogContainer.querySelector(
            ".clipboard-items-section div"
          );
          if (itemsGrid && itemsGrid.children.length === 0) {
            // Remove the entire section if no items left
            dialogContainer.querySelector(".clipboard-items-section").remove();
          }
        });
      }
    });

    itemEl.appendChild(deleteBtn);

    // Handle click to insert the block
    itemEl.addEventListener("click", () => {
      // Find the active stream
      const chooserContainer = dialogContainer.closest(
        "[data-streamfield-stream-container]"
      );

      // Close the dialog first
      closeInsertBlockDialog(dialogContainer);

      // Get current page ID
      const pageId = getPageId();

      if (!pageId) {
        console.error("Block Exchange: Could not determine current page ID");
        showNotification(
          "Could not determine page ID for inserting block",
          "error"
        );
        return;
      }

      // Insert the block
      insertClipboardItemToCurrentPage(item.id, pageId);
    });

    return itemEl;
  }

  // Fetch clipboard items via AJAX
  function fetchClipboardItems() {
    console.log("Block Exchange: Fetching clipboard items");

    return new Promise((resolve, reject) => {
      fetch("/admin/block-exchange/clipboard/list/")
        .then((response) => {
          console.log(
            "Block Exchange: Clipboard items response:",
            response.status
          );
          return response.json();
        })
        .then((data) => {
          console.log("Block Exchange: Clipboard items data:", data);
          if (data.success && data.items) {
            resolve(data.items);
          } else {
            reject(new Error("Failed to fetch clipboard items"));
          }
        })
        .catch((error) => {
          console.error(
            "Block Exchange: Error fetching clipboard items:",
            error
          );
          reject(error);
        });
    });
  }

  // Close the insert block dialog
  function closeInsertBlockDialog(dialogNode) {
    try {
      console.log("Block Exchange: Closing insert block dialog");

      // Find the dialog's close button
      const closeButton = dialogNode.querySelector(
        '.close, [data-dismiss], button[aria-label="Close"]'
      );
      if (closeButton) {
        console.log("Block Exchange: Clicking close button");
        closeButton.click();
        return true;
      }

      // If no close button, try removing the dialog directly
      const dialog = dialogNode.closest(".modal, .insert-block");
      if (dialog) {
        console.log("Block Exchange: Removing dialog from DOM");
        dialog.remove();
        return true;
      }

      console.warn("Block Exchange: Could not close insert block dialog");
      return false;
    } catch (err) {
      console.error("Block Exchange: Error closing insert block dialog:", err);
      return false;
    }
  }

  // Insert a clipboard item to the current page
  function insertClipboardItemToCurrentPage(clipboardId, pageId) {
    console.log("Block Exchange: Inserting clipboard item to current page", {
      clipboardId,
      pageId,
    });

    // Create form data
    const formData = new FormData();
    formData.append("clipboard_id", clipboardId);
    formData.append("page_id", pageId);

    // Get the CSRF token
    const csrfToken = document.querySelector(
      'input[name="csrfmiddlewaretoken"]'
    ).value;

    // Send the request
    fetch("/admin/block-exchange/paste/", {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
      },
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Block Exchange: Insert response:", data);
        if (data.success) {
          showNotification("Block inserted successfully", "success");

          // Refresh the page to show the new block
          // Using a small delay to ensure notification is seen
          setTimeout(() => {
            window.location.reload();
          }, 1500);
        } else {
          showNotification(
            "Failed to insert block: " + (data.error || "Unknown error"),
            "error"
          );
        }
      })
      .catch((error) => {
        console.error("Block Exchange: Error inserting block:", error);
        showNotification("Error inserting block: " + error, "error");
      });
  }

  // Try to run initialization immediately
  try {
    console.log("Block Exchange: Attempting immediate initialization");

    // Expose enhanceInsertBlockDialog globally so it can be called by the Wagtail hook
    window.enhanceInsertBlockDialog = enhanceInsertBlockDialog;

    initBlockExchange();

    // Also set up a DOMContentLoaded listener as a backup
    document.addEventListener("DOMContentLoaded", function () {
      console.log("Block Exchange: DOM content loaded, initializing");
      initBlockExchange();
    });

    // Add fallback initialization for cases where DOMContentLoaded already fired
    if (
      document.readyState === "complete" ||
      document.readyState === "interactive"
    ) {
      console.log(
        "Block Exchange: Document already loaded, initializing with delay"
      );
      // Small delay to ensure DOM is fully processed
      setTimeout(initBlockExchange, 100);
    }
  } catch (err) {
    console.error(
      "Block Exchange: Critical error during script execution:",
      err
    );
  }
})();
