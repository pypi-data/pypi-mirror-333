/**
 * API Client for Wagtail Block Exchange
 *
 * This module handles all API communication with the server-side endpoints
 * for the block exchange functionality.
 */

/**
 * Fetch the current user's clipboard items
 * @returns {Promise<Array>} Promise resolving to an array of clipboard items
 */
export function fetchClipboardItems() {
  return fetch("/admin/block-exchange/clipboard/list/")
    .then((response) => {
      if (!response.ok) {
        throw new Error(
          `Fetch failed with status ${response.status}: ${response.statusText}`
        );
      }
      return response.json();
    })
    .then((data) => {
      // Ensure we return an array of items in a consistent format
      if (data && data.items && Array.isArray(data.items)) {
        return data.items;
      } else if (data && Array.isArray(data)) {
        return data;
      }

      // If we get here, the data format is unexpected
      return [];
    })
    .catch((error) => {
      console.error("Error fetching clipboard items:", error);
      throw error;
    });
}

/**
 * Copy a block to the clipboard
 * @param {number} pageId - The page ID containing the block
 * @param {string} blockId - The block ID to copy
 * @param {string} label - Optional label for the block
 * @param {string} csrfToken - CSRF token for the request
 * @returns {Promise<Object>} Promise resolving to the copy operation result
 */
export function copyBlockToClipboard(pageId, blockId, label = "", csrfToken) {
  const formData = new FormData();
  formData.append("page_id", pageId);
  formData.append("block_id", blockId);
  formData.append("label", label);

  return fetch("/admin/block-exchange/copy/", {
    method: "POST",
    headers: { "X-CSRFToken": csrfToken },
    body: formData,
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(
          `Copy failed with status ${response.status}: ${response.statusText}`
        );
      }
      return response.json();
    })
    .then((data) => {
      return data;
    })
    .catch((error) => {
      console.error("Error copying block:", error);
      throw error;
    });
}

/**
 * Paste a block from the clipboard to a page
 * @param {number} clipboardId - The ID of the clipboard item
 * @param {number} pageId - The ID of the page to paste to
 * @param {string} csrfToken - The CSRF token for security
 * @param {string|null} fieldName - Optional specific field name to paste to (null for auto-detect)
 * @param {number} position - Position to insert the block at (-1 for end)
 * @returns {Promise<Object>} Promise resolving to the paste operation result
 */
export function pasteBlockToPage(
  clipboardId,
  pageId,
  csrfToken,
  fieldName = null,
  position = -1
) {
  const formData = new FormData();
  formData.append("clipboard_id", clipboardId);
  formData.append("page_id", pageId);

  if (fieldName) {
    formData.append("field_name", fieldName);
  }

  // Always include position parameter, even if it's the default -1
  formData.append("position", position);

  return fetch("/admin/block-exchange/paste/", {
    method: "POST",
    headers: { "X-CSRFToken": csrfToken },
    body: formData,
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(
          `Fetch failed with status ${response.status}: ${response.statusText}`
        );
      }
      return response.json();
    })
    .then((data) => {
      return data;
    })
    .catch((error) => {
      console.error("Error pasting block:", error);
      throw error;
    });
}

/**
 * Delete a clipboard item
 * @param {number} clipboardId - The clipboard item ID to delete
 * @param {string} csrfToken - CSRF token for the request
 * @returns {Promise<Object>} Promise resolving to the delete operation result
 */
export function deleteClipboardItem(clipboardId, csrfToken) {
  return fetch(`/admin/block-exchange/clipboard/clear/${clipboardId}/`, {
    method: "POST",
    headers: { "X-CSRFToken": csrfToken },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(
          `Delete failed with status ${response.status}: ${response.statusText}`
        );
      }
      return response.json();
    })
    .then((data) => {
      return data;
    })
    .catch((error) => {
      console.error("Error deleting clipboard item:", error);
      throw error;
    });
}

/**
 * Check if a block is compatible with a page
 * @param {number} clipboardId - The clipboard item ID
 * @param {number} pageId - The page ID to check against
 * @returns {Promise<Object>} Promise resolving to the compatibility check result
 */
export function checkBlockCompatibility(clipboardId, pageId) {
  return fetch(
    `/admin/block-exchange/compatibility-check/?clipboard_id=${clipboardId}&page_id=${pageId}`
  )
    .then((response) => {
      if (!response.ok) {
        throw new Error(
          `Compatibility check failed with status ${response.status}: ${response.statusText}`
        );
      }
      return response.json();
    })
    .then((data) => {
      return data;
    })
    .catch((error) => {
      console.error("Error checking compatibility:", error);
      throw error;
    });
}
