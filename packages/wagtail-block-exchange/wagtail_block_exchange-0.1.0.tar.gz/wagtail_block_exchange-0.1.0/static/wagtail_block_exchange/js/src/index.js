/**
 * Wagtail Block Exchange - Main Entry Point
 *
 * This file serves as the main entry point for the webpack build.
 * It imports and initializes all the necessary modules.
 */

// Import our CSS - disabled for now as we'll load it separately via Django
// import "../css/block-exchange.css";

// Import modules
import { blockChooserEnhancer } from "./block-chooser";
import "./clipboard-page"; // This will handle the clipboard page interactions

// Export public API
export { blockChooserEnhancer };
