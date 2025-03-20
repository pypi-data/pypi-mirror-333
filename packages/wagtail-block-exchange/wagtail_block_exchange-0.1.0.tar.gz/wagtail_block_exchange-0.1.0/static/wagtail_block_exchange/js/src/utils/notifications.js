/**
 * Notifications utility for Block Exchange
 *
 * Provides a consistent way to show notifications across the Block Exchange
 * functionality. It will try to use Wagtail's notification system if available,
 * and fall back to a custom implementation if not.
 */

/**
 * Check if Wagtail's notify function is available
 * @returns {boolean} True if available
 */
function hasWagtailNotify() {
  return (
    typeof window.wagtail !== "undefined" &&
    typeof window.wagtail.notify !== "undefined" &&
    typeof window.wagtail.notify.success === "function"
  );
}

/**
 * Create a custom notification element
 * @param {string} text - Notification text
 * @param {string} type - Notification type (success, error, warning, info)
 * @param {string} actionText - Optional action text
 * @param {string} actionUrl - Optional action URL
 * @returns {HTMLElement} Notification element
 */
function createCustomNotification(text, type, actionText, actionUrl) {
  // Create container if it doesn't exist
  let container = document.querySelector(".w-messages");
  if (!container) {
    container = document.createElement("div");
    container.className = "w-messages";
    container.style.cssText = `
      position: fixed;
      top: 10px;
      right: 10px;
      z-index: 9999;
      width: 300px;
    `;
    document.body.appendChild(container);
  }

  // Create notification
  const notification = document.createElement("div");
  notification.className = `w-messages__message w-messages__message--${type}`;
  notification.style.cssText = `
    margin-bottom: 10px;
    padding: 15px;
    border-radius: 3px;
    background-color: ${getBackgroundColor(type)};
    color: white;
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    display: flex;
    flex-direction: column;
    animation: slide-in 0.2s ease-out;
  `;

  // Content
  const content = document.createElement("div");
  content.className = "w-messages__message-content";
  content.textContent = text;
  content.style.cssText = `
    flex: 1;
    margin-bottom: ${actionText ? "10px" : "0"};
  `;
  notification.appendChild(content);

  // Action link if provided
  if (actionText && actionUrl) {
    const action = document.createElement("a");
    action.className = "w-messages__message-action";
    action.href = actionUrl;
    action.textContent = actionText;
    action.style.cssText = `
      display: inline-block;
      padding: 5px 10px;
      background-color: rgba(255,255,255,0.2);
      border-radius: 3px;
      color: white;
      text-decoration: none;
      font-weight: bold;
      align-self: flex-start;
    `;
    action.addEventListener("mouseover", () => {
      action.style.backgroundColor = "rgba(255,255,255,0.3)";
    });
    action.addEventListener("mouseout", () => {
      action.style.backgroundColor = "rgba(255,255,255,0.2)";
    });
    notification.appendChild(action);
  }

  // Close button
  const closeButton = document.createElement("button");
  closeButton.className = "w-messages__message-close";
  closeButton.innerHTML = "×";
  closeButton.style.cssText = `
    position: absolute;
    top: 5px;
    right: 5px;
    background: none;
    border: none;
    color: white;
    font-size: 18px;
    cursor: pointer;
    opacity: 0.7;
  `;
  closeButton.addEventListener("mouseover", () => {
    closeButton.style.opacity = "1";
  });
  closeButton.addEventListener("mouseout", () => {
    closeButton.style.opacity = "0.7";
  });
  closeButton.addEventListener("click", () => {
    notification.style.opacity = "0";
    setTimeout(() => {
      notification.remove();
    }, 200);
  });
  notification.appendChild(closeButton);

  // Add to container
  container.appendChild(notification);

  // Auto-remove after 5 seconds
  setTimeout(() => {
    notification.style.opacity = "0";
    setTimeout(() => {
      notification.remove();
    }, 200);
  }, 5000);

  return notification;
}

/**
 * Get background color for notification type
 * @param {string} type - Notification type
 * @returns {string} CSS color
 */
function getBackgroundColor(type) {
  switch (type) {
    case "success":
      return "#43b1b0";
    case "error":
      return "#cd3238";
    case "warning":
      return "#e9b04d";
    default:
      return "#666666";
  }
}

/**
 * Show a notification
 * @param {string} text - Notification text
 * @param {string} type - Notification type (success, error, warning, info)
 * @param {string} actionText - Optional action text
 * @param {string} actionUrl - Optional action URL
 */
function showNotification(
  text,
  type = "info",
  actionText = null,
  actionUrl = null
) {
  if (hasWagtailNotify()) {
    // Use Wagtail's notification system
    if (actionText && actionUrl) {
      window.wagtail.notify[type](text, {
        button: { text: actionText, url: actionUrl },
      });
    } else {
      window.wagtail.notify[type](text);
    }
  } else {
    // Use our custom notification
    createCustomNotification(text, type, actionText, actionUrl);
  }
}

/**
 * Show a success notification
 * @param {string} text - Notification text
 */
function showSuccess(text) {
  showNotification(text, "success");
}

/**
 * Show an error notification
 * @param {string} text - Notification text
 */
function showError(text) {
  showNotification(text, "error");
}

/**
 * Show a warning notification
 * @param {string} text - Notification text
 */
function showWarning(text) {
  showNotification(text, "warning");
}

/**
 * Show an info notification
 * @param {string} text - Notification text
 */
function showInfo(text) {
  showNotification(text, "info");
}

// Export the notification functions
export const notify = {
  show: showNotification,
  success: showSuccess,
  error: showError,
  warning: showWarning,
  info: showInfo,
};
