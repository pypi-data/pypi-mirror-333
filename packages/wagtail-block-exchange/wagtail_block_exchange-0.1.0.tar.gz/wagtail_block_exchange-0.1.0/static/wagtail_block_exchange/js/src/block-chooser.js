/**
 * Wagtail Block Exchange - Block Chooser Enhancement
 *
 * This module handles the enhancement of the Wagtail block chooser dialog
 * to include clipboard items for quick insertion.
 */

import { fetchClipboardItems, pasteBlockToPage } from "./utils/api-client.js";
import { notify } from "./utils/notifications.js";

// Main class for Block Chooser enhancement
class BlockChooserEnhancer {
  constructor() {
    // Configuration and state
    this.initialized = false;
    this.debug = false;
  }

  /**
   * Initialize the block chooser enhancement
   */
  initialize() {
    console.log("🔍 Block Exchange: Initializing block exchange functionality");

    try {
      // Find and process all add block buttons
      this.initAddBlockButtons();

      // Set up mutation observer for dynamic content
      this.setupMutationObserver();

      // Set up targeted mutation observer for streamfield containers
      this.setupStreamfieldObserver();

      // Check if we're coming from a paste operation (from clipboard page)
      this.checkForPendingPasteOperation();

      // Mark as initialized
      this.initialized = true;
      console.log("🔍 Block Exchange: Initialization complete");
    } catch (e) {
      console.error("🔍 Block Exchange: Error in initialization:", e);
    }
  }

  /**
   * Check if we're arriving at this page with a pending paste operation
   */
  checkForPendingPasteOperation() {
    try {
      const url = new URL(window.location.href);
      const hasPendingPaste = url.searchParams.has("clipboard_paste_pending");

      if (hasPendingPaste) {
        console.log("🔍 Block Exchange: Detected pending paste operation");

        // Check for unsaved changes
        const hasUnsavedChanges =
          document.querySelector(".w-status__indicator--dirty") !== null ||
          document.querySelector(".status-tag--draft") !== null;

        if (hasUnsavedChanges) {
          console.log(
            "🔍 Block Exchange: Unsaved changes detected with pending paste"
          );

          // Show a more prominent warning
          notify.warning(
            "This page has unsaved changes. Please save your changes before pasting any blocks to avoid data loss.",
            "warning"
          );

          // Find and highlight the save button
          const saveDraftButton = document.querySelector(
            '.action-save-draft, button[name="action-draft"]'
          );
          if (saveDraftButton) {
            saveDraftButton.style.animation = "pulse 1s infinite";
            saveDraftButton.style.boxShadow = "0 0 10px rgba(255, 165, 0, 0.8)";
            setTimeout(() => {
              saveDraftButton.style.animation = "";
              saveDraftButton.style.boxShadow = "";
            }, 5000);
          }
        }

        // Remove the parameter from the URL to prevent showing the warning again on refresh
        url.searchParams.delete("clipboard_paste_pending");
        window.history.replaceState({}, document.title, url.toString());
      }
    } catch (e) {
      console.error("🔍 Block Exchange: Error checking for pending paste:", e);
    }
  }

  /**
   * Set up a targeted mutation observer for streamfield containers
   */
  setupStreamfieldObserver() {
    try {
      console.log(
        "🔍 Block Exchange: Setting up streamfield container observer"
      );

      // First observe the body to detect when streamfield containers are added
      const bodyObserver = new MutationObserver((mutations) => {
        try {
          // Look for new streamfield containers
          mutations.forEach((mutation) => {
            if (mutation.addedNodes && mutation.addedNodes.length) {
              for (const node of mutation.addedNodes) {
                if (node.nodeType === 1) {
                  // Element node
                  // Check if this is a streamfield container
                  if (node.hasAttribute("data-streamfield-stream-container")) {
                    console.log(
                      "🔍 Block Exchange: Found new streamfield container",
                      node
                    );
                    this.observeStreamfieldContainer(node);
                  }

                  // Also check for streamfield containers within this node
                  const containers = node.querySelectorAll(
                    "[data-streamfield-stream-container]"
                  );
                  if (containers.length) {
                    console.log(
                      `🔍 Block Exchange: Found ${containers.length} streamfield containers in new node`
                    );
                    containers.forEach((container) =>
                      this.observeStreamfieldContainer(container)
                    );
                  }
                }
              }
            }
          });

          // Also check for existing streamfield containers
          const existingContainers = document.querySelectorAll(
            "[data-streamfield-stream-container]"
          );
          if (existingContainers.length) {
            console.log(
              `🔍 Block Exchange: Found ${existingContainers.length} existing streamfield containers`
            );
            existingContainers.forEach((container) =>
              this.observeStreamfieldContainer(container)
            );
          }
        } catch (e) {
          console.error(
            "🔍 Block Exchange: Error in bodyObserver callback:",
            e
          );
        }
      });

      // Start observing the body
      bodyObserver.observe(document.body, { childList: true, subtree: true });

      // Also observe existing streamfield containers right away
      const existingContainers = document.querySelectorAll(
        "[data-streamfield-stream-container]"
      );
      if (existingContainers.length) {
        console.log(
          `🔍 Block Exchange: Found ${existingContainers.length} existing streamfield containers during initial setup`
        );
        existingContainers.forEach((container) =>
          this.observeStreamfieldContainer(container)
        );
      }

      console.log("🔍 Block Exchange: Streamfield container observer set up");
    } catch (e) {
      console.error(
        "🔍 Block Exchange: Error setting up streamfield observer:",
        e
      );
    }
  }

  /**
   * Observe a single streamfield container for tippy panels
   * @param {Element} container - The streamfield container to observe
   */
  observeStreamfieldContainer(container) {
    try {
      // Check if already observed
      if (container.hasAttribute("data-block-exchange-observed")) {
        console.log(
          "🔍 Block Exchange: Streamfield container already observed, skipping"
        );
        return;
      }

      console.log(
        "🔍 Block Exchange: Setting up observer for streamfield container:",
        container
      );

      // Mark as observed
      container.setAttribute("data-block-exchange-observed", "true");

      // Create a new observer for this container
      const containerObserver = new MutationObserver((mutations) => {
        try {
          mutations.forEach((mutation) => {
            if (mutation.addedNodes && mutation.addedNodes.length) {
              for (const node of mutation.addedNodes) {
                if (node.nodeType === 1) {
                  // Element node
                  // Check for tippy elements and block chooser elements
                  const isTippy =
                    node.classList &&
                    (node.classList.contains("tippy-box") ||
                      node.hasAttribute("data-tippy-root") ||
                      node.classList.contains("tippy-content"));

                  const hasBlockChooser =
                    node.querySelector &&
                    (node.querySelector(
                      ".w-combobox, .w-combobox-container, .block-type, .block-help"
                    ) ||
                      node.innerHTML.includes("Insert content") ||
                      node.innerHTML.includes("block chooser") ||
                      node.innerHTML.includes("w-combobox__menu"));

                  // Log all elements for debugging
                  console.log(
                    "🔍 Block Exchange: New node in streamfield container:",
                    {
                      tagName: node.tagName,
                      id: node.id,
                      className: node.className,
                      isTippy: isTippy,
                      hasBlockChooser: hasBlockChooser,
                    }
                  );

                  if (isTippy || hasBlockChooser) {
                    console.log(
                      "🔍 Block Exchange: Found tippy or block chooser element in streamfield container!",
                      node
                    );

                    // Check if the element needs enhancement
                    if (!node.hasAttribute("data-block-exchange-processed")) {
                      console.log(
                        "🔍 Block Exchange: Enhancing newly detected tippy/block chooser"
                      );

                      // Wait a tiny bit for the content to be fully rendered
                      setTimeout(() => {
                        try {
                          this.enhanceBlockDialog(node);

                          // Also check inside - direct tippy elements often contain the actual dialog
                          const innerDialogs = node.querySelectorAll(
                            ".w-dialog, .w-streamfield-add-dialog, .choose-block, .w-combobox-container"
                          );
                          if (innerDialogs.length > 0) {
                            console.log(
                              `🔍 Block Exchange: Found ${innerDialogs.length} inner dialogs to enhance`
                            );
                            innerDialogs.forEach((dialog) => {
                              if (
                                !dialog.hasAttribute(
                                  "data-block-exchange-processed"
                                )
                              ) {
                                this.enhanceBlockDialog(dialog);
                              }
                            });
                          }
                        } catch (e) {
                          console.error(
                            "🔍 Block Exchange: Error enhancing tippy/block chooser:",
                            e
                          );
                        }
                      }, 50);
                    }
                  }
                }
              }
            }
          });
        } catch (e) {
          console.error(
            "🔍 Block Exchange: Error in containerObserver callback:",
            e
          );
        }
      });

      // Start observing the container for changes
      containerObserver.observe(container, {
        childList: true, // Watch for child nodes being added or removed
        subtree: true, // Watch all descendants, not just direct children
      });

      console.log(
        "🔍 Block Exchange: Streamfield container observer started for:",
        container
      );
    } catch (e) {
      console.error(
        "🔍 Block Exchange: Error observing streamfield container:",
        e
      );
    }
  }

  /**
   * Initialize the add block buttons
   */
  initAddBlockButtons() {
    try {
      // Use multiple selectors to find all possible add buttons
      const selectors = [
        "button.c-sf-add-button",
        'button[title="Insert a block"]',
        ".c-sf-add-button",
        ".c-sf-container__add-button",
        "button.w-streamfield-add",
        "[data-streamfield-block-add]",
        ".c-sf-add-panel",
      ];

      const selectorString = selectors.join(", ");
      console.log(
        "🔍 Block Exchange: Looking for buttons with selectors:",
        selectorString
      );

      const addButtons = document.querySelectorAll(selectorString);
      console.log(
        `🔍 Block Exchange: Found ${addButtons.length} add block buttons`
      );

      // Log details about each button found
      addButtons.forEach((button, index) => {
        try {
          console.log(`🔍 Block Exchange: Button ${index} details:`, {
            tagName: button.tagName,
            id: button.id,
            className: button.className,
            title: button.getAttribute("title"),
            innerHTML: button.innerHTML.substring(0, 50) + "...",
          });

          // Skip if already processed
          if (button.hasAttribute("data-block-exchange-processed")) {
            console.log(
              `🔍 Block Exchange: Button ${index} already processed, skipping`
            );
            return;
          }

          // Mark as processed
          button.setAttribute("data-block-exchange-processed", "true");

          // Add visual indicator for debugging
          button.setAttribute("data-debug-block-exchange", "monitored");

          // Add click handler
          button.addEventListener("click", (e) => {
            try {
              console.log(
                "🔍 Block Exchange: Add block button clicked!",
                e.target
              );
              console.log("🔍 Block Exchange: Button details:", {
                tagName: this.tagName,
                id: this.id,
                className: this.className,
                title: this.getAttribute("title"),
              });

              // Alert for debugging in case console is not visible
              if (this.debug) {
                alert("Block Exchange: Button clicked!");
              }

              // Wait for tippy tooltip to be created
              console.log("🔍 Block Exchange: Waiting for dialog to appear...");
              setTimeout(() => this.findAndEnhanceBlockDialog(), 100);

              // Also try again after a longer delay in case of slow rendering
              setTimeout(() => this.findAndEnhanceBlockDialog(), 500);
              setTimeout(() => this.findAndEnhanceBlockDialog(), 1000);
            } catch (e) {
              console.error("🔍 Block Exchange: Error in click handler:", e);
            }
          });

          console.log(
            `🔍 Block Exchange: Added click handler to button ${index}`
          );
        } catch (e) {
          console.error(
            `🔍 Block Exchange: Error processing button ${index}:`,
            e
          );
        }
      });

      // Also try the direct approach for newer Wagtail versions
      document.addEventListener("wagtail:blocks-chooser-ready", (e) => {
        console.log(
          "🔍 Block Exchange: Detected wagtail:blocks-chooser-ready event!",
          e
        );

        // The chooser should be available in e.detail for newer Wagtail versions
        const chooser = e.detail && e.detail.chooser;
        if (chooser) {
          console.log("🔍 Block Exchange: Got chooser from event", chooser);
          // Try to find the dialog element
          const dialogElement =
            chooser.element ||
            chooser.popup ||
            document.querySelector(".tippy-box");
          if (dialogElement) {
            console.log(
              "🔍 Block Exchange: Found dialog element from event",
              dialogElement
            );
            this.enhanceBlockDialog(dialogElement);
          }
        }

        // Also do a general search for any open dialogs
        this.findAndEnhanceBlockDialog();
      });
    } catch (e) {
      console.error("🔍 Block Exchange: Error in initAddBlockButtons:", e);
    }
  }

  /**
   * Find and enhance the block chooser dialog
   * @returns {boolean} Whether a dialog was found and enhanced
   */
  findAndEnhanceBlockDialog() {
    try {
      console.log("🔍 Block Exchange: Looking for block dialog");

      // Look for all possible dialog/tooltip elements
      const selectors = [
        ".tippy-box",
        ".tippy-content",
        "[data-tippy-root]",
        '[data-state="visible"]',
        ".w-dialog",
        ".w-streamfield-add-dialog",
        ".choose-block",
        ".w-combobox-container",
        '[aria-labelledby="wagtail-chooser-title"]',
      ];

      const elements = document.querySelectorAll(selectors.join(", "));
      console.log(
        `🔍 Block Exchange: Found ${elements.length} possible dialog elements`
      );

      let dialogFound = false;

      elements.forEach((element, index) => {
        try {
          console.log(`🔍 Block Exchange: Checking element ${index}:`, {
            tagName: element.tagName,
            id: element.id,
            className: element.className,
            visible: element.offsetParent !== null,
          });

          // Skip if already processed
          if (element.hasAttribute("data-block-exchange-processed")) {
            console.log(
              `🔍 Block Exchange: Element ${index} already processed, skipping`
            );
            return;
          }

          // Mark as processed
          element.setAttribute("data-block-exchange-processed", "true");

          // Check for block chooser content
          const hasBlockContent =
            element.querySelector(
              ".w-combobox, .w-combobox-container, .block-type, .block-help"
            ) ||
            element.querySelector('[aria-labelledby="downshift"]') ||
            element.innerHTML.includes('aria-labelledby="downshift') ||
            element.innerHTML.includes('class="w-combobox') ||
            element.innerHTML.includes("Insert content") ||
            element.innerHTML.includes("block chooser") ||
            element.innerHTML.includes("w-combobox__menu");

          if (hasBlockContent) {
            console.log(
              `🔍 Block Exchange: Found block dialog in element ${index}`
            );
            this.enhanceBlockDialog(element);
            dialogFound = true;
          } else {
            console.log(
              `🔍 Block Exchange: Element ${index} is not a block dialog`
            );
          }
        } catch (e) {
          console.error(
            `🔍 Block Exchange: Error processing element ${index}:`,
            e
          );
        }
      });

      // If we still don't find the dialog, log this information
      if (!dialogFound) {
        console.log("🔍 Block Exchange: No block dialog found in this pass");
      }

      return dialogFound;
    } catch (e) {
      console.error(
        "🔍 Block Exchange: Error in findAndEnhanceBlockDialog:",
        e
      );
      return false;
    }
  }

  /**
   * Enhance the block dialog with clipboard functionality
   * @param {Element} dialog - The dialog element to enhance
   */
  enhanceBlockDialog(dialog) {
    try {
      // Mark this dialog to prevent it from being processed multiple times
      const isAlreadyProcessed = dialog.hasAttribute(
        "data-block-exchange-processed"
      );

      if (isAlreadyProcessed) {
        return;
      }

      // Mark dialog as processed immediately to prevent double processing
      dialog.setAttribute("data-block-exchange-processed", "true");

      // Try to identify the insert position from the dialog or parent StreamField
      let insertPosition = -1;
      try {
        // Find the parent stream block
        const streamField = dialog.closest(
          "[data-streamfield-stream-container]"
        );

        if (streamField) {
          // Look for the "add" button that triggered this dialog
          const addButtons = streamField.querySelectorAll(".c-sf-add-button");

          // Convert to array for easier handling
          const addButtonsList = Array.from(addButtons);

          // Check which add button is closest to the dialog
          for (let i = 0; i < addButtonsList.length; i++) {
            if (addButtonsList[i].classList.contains("insert-action-running")) {
              // This is likely the button that triggered the dialog
              insertPosition = i;
              break;
            }
          }

          if (insertPosition === -1) {
            for (let i = 0; i < addButtonsList.length; i++) {
              const btn = addButtonsList[i];
              if (
                btn.classList.contains("active") ||
                btn.classList.contains("focused") ||
                btn === document.activeElement
              ) {
                insertPosition = i;
                break;
              }
            }
          }

          if (insertPosition === -1) {
            // Try to find the position from the streamfield or dialog
            const dialogPosition =
              dialog.dataset.position ||
              dialog.getAttribute("data-position") ||
              streamField.dataset.currentPosition ||
              streamField.getAttribute("data-current-position");

            if (dialogPosition) {
              insertPosition = parseInt(dialogPosition, 10);
            }
          }
        }
      } catch (posErr) {
        console.error(
          "Block Exchange: Error determining insert position:",
          posErr
        );
      }

      // Store the position in the dialog for later use
      dialog.dataset.insertPosition = insertPosition;

      // Now check for existing clipboard sections and remove them
      // (both within w-combobox-container and at the same level)
      const allClipboardSections =
        dialog.querySelectorAll(".clipboard-section");

      allClipboardSections.forEach((section) => {
        section.remove();
      });

      // Now also remove any blue/dark sections that might be clipboard sections
      const allDivs = dialog.querySelectorAll("div");
      for (const div of allDivs) {
        if (div === dialog) continue;

        const style = window.getComputedStyle(div);
        const bgColor = style.backgroundColor;

        if (
          bgColor &&
          (bgColor.includes("rgb(0, 125, 126)") ||
            bgColor.includes("#007d7e") ||
            bgColor.includes("rgb(0, 89, 90)") ||
            bgColor.includes("#00595a"))
        ) {
          div.remove();
        }
      }

      // Now add ONE clipboard section - only to the combobox container, not to the dialog itself
      const comboboxContainer = dialog.querySelector(".w-combobox-container");

      if (comboboxContainer) {
        this.addClipboardSection(comboboxContainer, insertPosition);
      } else {
        // As a fallback, try other menu containers
        const menuContainer = dialog.querySelector(
          ".w-combobox__menu-container, .w-combobox__menu"
        );

        if (menuContainer) {
          this.addClipboardSection(menuContainer, insertPosition);
        } else {
          // Last resort: add to dialog content, but NOT to the dialog itself
          const dialogContent = dialog.querySelector(
            ".w-dialog__content, .tippy-content"
          );

          if (dialogContent) {
            this.addClipboardSection(dialogContent, insertPosition);
          }
        }
      }
    } catch (e) {
      console.error("Block Exchange: Error in enhanceBlockDialog:", e);
    }
  }

  /**
   * Add the clipboard section to a container
   * @param {Element} container - The container to add the clipboard section to
   */
  addClipboardSection(container, insertPosition = -1) {
    try {
      console.log(
        "🔍 Block Exchange: Adding clipboard section to container at position",
        insertPosition,
        container
      );

      // Create clipboard section
      const section = document.createElement("div");
      section.className = "clipboard-section";
      section.dataset.insertPosition = insertPosition;
      section.style.cssText = `
                margin-top: 20px;
                padding-top: 10px;
                border-top: 1px solid rgba(0,0,0,0.1);
            `;

      // Add heading
      const heading = document.createElement("h4");
      heading.textContent = "Clipboard Items";
      heading.style.cssText = `
                margin: 0 0 10px 0;
                padding: 0 10px;
                font-size: 16px;
                font-weight: 600;
                color: #007d7e;
            `;
      section.appendChild(heading);

      // Add loader
      const loader = document.createElement("div");
      loader.className = "clipboard-loader";
      loader.style.cssText = "padding: 10px; text-align: center;";
      loader.textContent = "Loading clipboard items...";
      section.appendChild(loader);

      // Try to insert the section
      try {
        container.appendChild(section);
        console.log("🔍 Block Exchange: Clipboard section added successfully");

        // Load clipboard items
        this.loadClipboardItems(section, insertPosition);
      } catch (e) {
        console.error("🔍 Block Exchange: Failed to add clipboard section", e);

        // Try a different approach - maybe the container is not a valid parent
        if (container.parentElement) {
          try {
            container.parentElement.appendChild(section);
            console.log(
              "🔍 Block Exchange: Added clipboard section to parent instead"
            );
            this.loadClipboardItems(section, insertPosition);
          } catch (e2) {
            console.error(
              "🔍 Block Exchange: Failed to add to parent as well",
              e2
            );
          }
        }
      }
    } catch (e) {
      console.error("🔍 Block Exchange: Error in addClipboardSection:", e);
    }
  }

  /**
   * Load clipboard items via AJAX
   * @param {Element} section - The clipboard section element
   */
  loadClipboardItems(section, insertPosition = -1) {
    try {
      console.log(
        "🔍 Block Exchange: Loading clipboard items for position",
        insertPosition
      );

      // Check if there are unsaved changes ONLY for the actual page editor
      // (not for the insert block dialog)
      const isInsertDialog =
        section.closest(".tippy-content") !== null ||
        section.closest(".tippy-box") !== null ||
        section.closest(".w-dialog") !== null;

      const hasUnsavedChanges =
        document.querySelector(".w-status__indicator--dirty") !== null ||
        document.querySelector(".status-tag--draft") !== null ||
        document.querySelector(
          '[data-side-panel-toggle="comments"].w-status__indicator--dirty'
        ) !== null;

      // Only show warning in actual page, not in insert dialog
      if (hasUnsavedChanges && !isInsertDialog) {
        // Show message to save first
        section.innerHTML = "";
        const warningDiv = document.createElement("div");
        warningDiv.className = "clipboard-warning";
        warningDiv.style.cssText = `
          background-color: #fff3cd;
          color: #856404;
          padding: 10px;
          border-radius: 3px;
          margin: 10px;
          font-size: 14px;
        `;
        warningDiv.textContent =
          "Please save your changes before pasting a block from the clipboard. Pasting with unsaved changes can cause unpredictable results.";
        section.appendChild(warningDiv);
        return;
      }

      // Get the clipboard items
      fetchClipboardItems()
        .then((data) => {
          console.log("🔍 Block Exchange: Raw clipboard data received:", data);

          // DEBUGGING: Log the type and structure of the data
          console.log("🔍 Block Exchange: Data type:", typeof data);
          console.log(
            "🔍 Block Exchange: Data has items property:",
            data && data.items !== undefined
          );

          // Try to extract items from various data formats
          let items = [];
          if (data && data.items && Array.isArray(data.items)) {
            // Format: {items: [...]}
            items = data.items;
          } else if (data && Array.isArray(data)) {
            // Format: [...]
            items = data;
          } else if (data && typeof data === "object") {
            // Last resort - try to extract items as object values
            console.log(
              "🔍 Block Exchange: Attempting to extract object values as items"
            );
            const values = Object.values(data);
            if (values.length > 0 && typeof values[0] === "object") {
              items = values;
            }
          }

          console.log("🔍 Block Exchange: Processed items:", items);

          // Safety check - ensure items is an array
          if (!Array.isArray(items)) {
            console.error(
              "🔍 Block Exchange: Items is not an array, creating empty array instead"
            );
            items = [];
          }

          // Remove loader
          section.innerHTML = "";

          // Add heading back
          const heading = document.createElement("h4");
          heading.textContent = "Clipboard Items";
          heading.style.cssText = `
              margin: 0 0 10px 0;
              padding: 0 10px;
              font-size: 16px;
              font-weight: 600;
              color: #007d7e;
            `;
          section.appendChild(heading);

          // Handle empty items
          if (!items || items.length === 0) {
            const emptyMessage = document.createElement("div");
            emptyMessage.style.cssText =
              "padding: 10px; text-align: center; color: #666;";
            emptyMessage.textContent = "No items in clipboard";
            section.appendChild(emptyMessage);
            return;
          }

          // Create grid for items
          const grid = document.createElement("div");
          grid.style.cssText = `
              display: grid;
              grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
              grid-gap: 10px;
              padding: 0 10px;
            `;
          section.appendChild(grid);

          // Create items
          items.forEach((item) => {
            // Safety check - ensure item is an object
            if (!item || typeof item !== "object") {
              console.warn("🔍 Block Exchange: Invalid item, skipping:", item);
              return;
            }

            const itemEl = document.createElement("div");
            itemEl.className = "clipboard-item";
            itemEl.style.cssText = `
                background-color: #fff;
                border: 1px solid #e6e6e6;
                border-radius: 3px;
                padding: 10px;
                cursor: pointer;
              `;

            // Add hover effect
            itemEl.addEventListener("mouseover", () => {
              itemEl.style.boxShadow = "0 2px 4px rgba(0,0,0,0.1)";
              itemEl.style.borderColor = "#007d7e";
            });
            itemEl.addEventListener("mouseout", () => {
              itemEl.style.boxShadow = "none";
              itemEl.style.borderColor = "#e6e6e6";
            });

            // Add name - formatted to match clipboard page
            const name = document.createElement("div");
            name.style.cssText = `
                font-weight: bold;
                margin-bottom: 5px;
              `;

            // Format title to match clipboard page format
            let titleText = "";

            // Check if it has a custom label that's not a default "Block from page" label
            if (item.label && !item.label.includes("Block from page")) {
              titleText = item.label;
            } else {
              // Format: "{block_type} block from page {page_title} ({page_id})"
              const blockType =
                item.block_type_display || item.block_type || "Unknown";
              const pageTitle = item.source_page_title || "Page";
              const pageId = item.source_page || "?";

              titleText = `${blockType} block from page ${pageTitle} (${pageId})`;
            }

            name.textContent = titleText;
            itemEl.appendChild(name);

            // Add type
            const type = document.createElement("div");
            type.style.cssText = `
                font-size: 12px;
                color: #666;
                margin-bottom: 5px;
              `;
            type.textContent =
              item.block_type_display || item.block_type || "Unknown type";
            itemEl.appendChild(type);

            // Handle click
            itemEl.addEventListener("click", () => {
              console.log(
                "🔍 Block Exchange: Item clicked with position",
                insertPosition,
                item
              );
              this.insertClipboardItem(item, insertPosition);
            });

            grid.appendChild(itemEl);
          });

          console.log("🔍 Block Exchange: Loaded and rendered clipboard items");
        })
        .catch((error) => {
          console.error(
            "🔍 Block Exchange: Error loading clipboard items",
            error
          );
          section.innerHTML = `
            <div style="padding: 10px; color: #721c24; background-color: #f8d7da; border: 1px solid #f5c6cb; border-radius: 3px;">
              Error loading clipboard items: ${error.message}
            </div>
          `;
        });
    } catch (e) {
      console.error("🔍 Block Exchange: Error in loadClipboardItems:", e);

      // Show a more graceful error in the section
      if (section) {
        section.innerHTML = `
          <div style="padding: 10px; color: #721c24; background-color: #f8d7da; border: 1px solid #f5c6cb; border-radius: 3px;">
            Error loading clipboard items: ${e.message}
          </div>
        `;
      }
    }
  }

  /**
   * Insert a clipboard item
   * @param {Object} item - The clipboard item to insert
   */
  insertClipboardItem(item, insertPosition = -1) {
    try {
      console.log(
        "🔍 Block Exchange: Inserting clipboard item at position",
        insertPosition,
        item
      );

      // Get page ID from URL
      const match = window.location.pathname.match(
        /\/admin\/pages\/(\d+)\/edit\/?/
      );
      if (!match) {
        console.error("🔍 Block Exchange: Could not determine page ID");
        notify.error("Could not determine page ID");
        return;
      }

      const pageId = match[1];
      console.log("🔍 Block Exchange: Page ID", pageId);

      // Get CSRF token
      const csrfToken = document.querySelector(
        'input[name="csrfmiddlewaretoken"]'
      ).value;
      if (!csrfToken) {
        console.error("🔍 Block Exchange: No CSRF token found");
        notify.error("No CSRF token found");
        return;
      }

      // Close all tippy tooltips
      document.querySelectorAll("[data-tippy-root]").forEach((el) => {
        el.remove();
      });

      // First, check if there are unsaved changes
      const hasUnsavedChanges =
        document.querySelector(".w-status__indicator--dirty") !== null ||
        document.querySelector(".status-tag--draft") !== null;

      // If there are unsaved changes, BLOCK pasting and show a notification
      if (hasUnsavedChanges) {
        console.log(
          "🔍 Block Exchange: Unsaved changes detected, blocking paste operation"
        );

        notify.warning(
          "Please save your changes before pasting a block. Pasting with unsaved changes can cause conflicts."
        );

        // Find and highlight the save button to guide the user
        const saveDraftButton = document.querySelector(
          'button[data-action="submit"]'
        );
        if (saveDraftButton) {
          saveDraftButton.style.animation = "pulse 1s infinite";
          setTimeout(() => {
            saveDraftButton.style.animation = "";
          }, 3000);
        }

        return;
      }

      // Show notification about what's happening
      notify.info("Inserting block...");

      // Perform the paste operation
      this.performPasteOperation(item, pageId, csrfToken, insertPosition);
    } catch (e) {
      console.error("🔍 Block Exchange: Error in insertClipboardItem:", e);
      notify.error("Error inserting block: " + e.message);
    }
  }

  /**
   * Helper function to perform the actual paste operation
   * @param {Object} item - The clipboard item to paste
   * @param {string} pageId - The page ID to paste to
   * @param {string} csrfToken - The CSRF token for the request
   * @param {number} position - The position to insert at (-1 for append)
   */
  performPasteOperation(item, pageId, csrfToken, position = -1) {
    // Double-check for unsaved changes again right before paste operation
    const hasUnsavedChanges =
      document.querySelector(".w-status__indicator--dirty") !== null ||
      document.querySelector(".status-tag--draft") !== null ||
      document.querySelector(
        '[data-side-panel-toggle="comments"].w-status__indicator--dirty'
      ) !== null;

    if (hasUnsavedChanges) {
      notify.warning(
        "Please save your changes before pasting blocks. Pasting with unsaved changes can cause conflicts."
      );
      return;
    }

    // Get the item ID
    const clipboardId = item.id;

    // Perform the paste operation via API
    pasteBlockToPage(clipboardId, pageId, csrfToken, null, position)
      .then((data) => {
        if (data.success) {
          notify.success("Block inserted successfully");

          // Reload page to show the inserted block
          window.location.reload();
        } else {
          notify.error(data.error || "Error inserting block");
        }
      })
      .catch((error) => {
        notify.error("Error inserting block: " + error.message);
      });
  }

  /**
   * Set up a mutation observer to watch for new add block buttons being added
   */
  setupMutationObserver() {
    try {
      console.log("🔍 Block Exchange: Setting up mutation observer");

      const observer = new MutationObserver((mutations) => {
        try {
          let shouldInit = false;
          let newDialog = false;

          for (const mutation of mutations) {
            if (mutation.addedNodes && mutation.addedNodes.length) {
              for (const node of mutation.addedNodes) {
                if (node.nodeType === 1) {
                  // Element node
                  // Check for buttons
                  const isAddButton =
                    node.classList &&
                    (node.classList.contains("c-sf-add-button") ||
                      (node.hasAttribute("title") &&
                        node.getAttribute("title") === "Insert a block"));

                  const hasAddButton =
                    node.querySelector &&
                    node.querySelector(
                      'button.c-sf-add-button, button[title="Insert a block"]'
                    );

                  // Check for dialog/tippy elements
                  const isTippy =
                    node.classList &&
                    (node.classList.contains("tippy-box") ||
                      node.hasAttribute("data-tippy-root"));

                  const hasTippy =
                    node.querySelector &&
                    node.querySelector(".tippy-box, [data-tippy-root]");

                  if (isAddButton || hasAddButton) {
                    console.log(
                      "🔍 Block Exchange: Mutation observer detected new button"
                    );
                    shouldInit = true;
                  }

                  if (isTippy || hasTippy) {
                    console.log(
                      "🔍 Block Exchange: Mutation observer detected new dialog/tippy"
                    );
                    newDialog = true;
                  }
                }
              }
            }
          }

          if (shouldInit) {
            console.log(
              "🔍 Block Exchange: Detected new add buttons, reinitializing"
            );
            setTimeout(() => this.initAddBlockButtons(), 100);
          }

          if (newDialog) {
            console.log(
              "🔍 Block Exchange: Detected new dialog elements, looking for block chooser"
            );
            setTimeout(() => this.findAndEnhanceBlockDialog(), 100);
          }
        } catch (e) {
          console.error(
            "🔍 Block Exchange: Error in mutation observer callback:",
            e
          );
        }
      });

      // Start observing for new elements
      observer.observe(document.body, { childList: true, subtree: true });

      console.log("🔍 Block Exchange: Mutation observer set up successfully");
    } catch (e) {
      console.error(
        "🔍 Block Exchange: Error setting up mutation observer:",
        e
      );
    }
  }

  /**
   * Toggle debug mode
   * @returns {boolean} The new debug state
   */
  toggleDebug() {
    this.debug = !this.debug;
    console.log(
      "🔍 Block Exchange: Debug mode",
      this.debug ? "enabled" : "disabled"
    );
    return this.debug;
  }

  /**
   * Debug method to find all streamfields
   * @returns {NodeList} All streamfield containers
   */
  findStreamfields() {
    const containers = document.querySelectorAll(
      "[data-streamfield-stream-container]"
    );
    console.log("🔍 Block Exchange: Found streamfield containers:", containers);
    return containers;
  }

  /**
   * Debug method to log all add buttons
   * @returns {NodeList} All add buttons
   */
  logButtons() {
    const buttons = document.querySelectorAll(
      'button.c-sf-add-button, button[title="Insert a block"]'
    );
    console.log("🔍 Block Exchange: All add buttons:", buttons);
    return buttons;
  }
}

// Create and export the BlockChooserEnhancer instance
const blockChooserEnhancer = new BlockChooserEnhancer();

// Export for global access (for debugging)
if (typeof window !== "undefined") {
  window.debugBlockExchange = {
    logButtons: () => blockChooserEnhancer.logButtons(),
    checkDialog: () => blockChooserEnhancer.findAndEnhanceBlockDialog(),
    toggleDebug: () => blockChooserEnhancer.toggleDebug(),
    findStreamfields: () => blockChooserEnhancer.findStreamfields(),
  };
}

// Initialize when the DOM is fully loaded
document.addEventListener("DOMContentLoaded", () => {
  console.log("🔍 Block Exchange: Script loaded - ENHANCED MODULE VERSION");

  // Global error handler for JavaScript errors
  window.addEventListener("error", function (e) {
    console.error(
      "🔍 Block Exchange: Global error caught:",
      e.message,
      e.filename,
      e.lineno
    );
    // Don't prevent default for all errors, only storage access errors
    if (e.message && e.message.includes("Access to storage is not allowed")) {
      console.warn("🔍 Block Exchange: Storage access error suppressed");
      e.preventDefault();
      e.stopPropagation();
    }
  });

  // Wait a bit to ensure Wagtail's UI is fully loaded
  setTimeout(() => {
    try {
      console.log("🔍 Block Exchange: Delayed initialization starting");
      blockChooserEnhancer.initialize();
    } catch (e) {
      console.error("🔍 Block Exchange: Error in delayed initialization:", e);
    }
  }, 1000);
});

export { blockChooserEnhancer };
