import { app } from "../../../scripts/app.js";
import { api } from "../../../scripts/api.js";

// Helper function to find a widget by name
const findWidgetByName = (node, name) => {
  return node.widgets ? node.widgets.find((w) => w.name === name) : null;
};

// Helper function to get widget value
const getWidgetValue = (node, widgetName) => {
  // First try to get value from widget directly
  const widget = findWidgetByName(node, widgetName);
  if (widget && widget.value !== undefined && widget.value !== null) {
    return widget.value;
  }

  // Fallback to DOM search if widget not found
  const allInputs = document.querySelectorAll("input[type='text'], textarea");
  const visibleInputs = [];
  for (const input of allInputs) {
    const rect = input.getBoundingClientRect();
    const isVisible = rect.width > 0 && rect.height > 0;
    if (isVisible) {
      visibleInputs.push(input);
    }
  }

  // Try to find by value pattern
  for (const input of visibleInputs) {
    const value = input.value;
    if (widgetName === "base_url" && value && (value.startsWith("http://") || value.startsWith("https://"))) {
      return value;
    }
    if (widgetName === "api_key" && value && value.length > 0) {
      return value;
    }
  }

  return "";
};

// Helper function to safely update combo widget options
const updateComboWidgetOptions = (node, widgetName, newOptions) => {
  if (!node || !newOptions || newOptions.length === 0) return false;
  try {
    const oldWidgetIndex = node.widgets.findIndex(w => w.name === widgetName);
    if (oldWidgetIndex === -1) {
      console.error(`[LLM Party] Widget '${widgetName}' not found`);
      return false;
    }

    const oldWidget = node.widgets[oldWidgetIndex];
    const currentValue = oldWidget.value;
    const defaultValue = newOptions.includes(currentValue) ? currentValue : newOptions[0];

    // Remove old widget
    oldWidget.onRemove?.();
    node.widgets.splice(oldWidgetIndex, 1);

    // Create new COMBO widget (insert at the same position to preserve order)
    const newWidget = node.addWidget("combo", widgetName, defaultValue, () => {}, { values: newOptions });
    node.widgets.splice(node.widgets.indexOf(newWidget), 1);
    node.widgets.splice(oldWidgetIndex, 0, newWidget);

    node.setDirtyCanvas(true, true);
    if (node.graph) {
      node.graph.setDirtyCanvas(true, true);
    }
    console.log(`[LLM Party] Replaced '${widgetName}' widget with combo (${newOptions.length} items)`);
    return true;
  } catch (e) {
    console.error(`[LLM Party] Error updating widget options:`, e);
    return false;
  }
};

// Store button state per node
const nodeButtonState = new WeakMap();

// ComfyUI Extension for LLM_api_loader node
app.registerExtension({
  name: "Comfy.LLMParty.LLMApiLoader",

  async beforeRegisterNodeDef(nodeType, nodeData, app) {
    if (nodeData.name === "LLM_api_loader") {
      const onNodeCreated = nodeType.prototype.onNodeCreated;
      nodeType.prototype.onNodeCreated = function() {
        const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
        const node = this;
        setTimeout(() => {
          try {
            console.log("[LLM Party] Adding Get Models button for LLM_api_loader node");
            createOrUpdateButton(node, "Get Models");
          } catch (e) {
            console.error("Error adding Get Models button:", e);
          }
        }, 100);
        return r;
      };
    }
  }
});

// Function to create or update the button
function createOrUpdateButton(node, buttonText) {
  // Remove ALL existing Get Models buttons
  if (node.widgets) {
    const buttonsToRemove = node.widgets.filter(w => w.type === "button" && w.name === "Get Models");
    for (let i = buttonsToRemove.length - 1; i >= 0; i--) {
      const button = buttonsToRemove[i];
      const idx = node.widgets.indexOf(button);
      if (idx !== -1) {
        node.widgets.splice(idx, 1);
      }
    }
  }

  // Get or create button state for this node
  let state = nodeButtonState.get(node);
  if (!state) {
    state = { isProcessing: false };
    nodeButtonState.set(node, state);
  }

  // Create button widget - in LiteGraph: addWidget(type, name, value, callback)
  // For button: type="button", name=internal name, value=display text, callback=click handler
  const updateButton = node.addWidget("button", "Get Models", buttonText, async () => {
    if (state.isProcessing) {
      console.log("[LLM Party] Button click already processing, ignoring");
      return;
    }

    console.log("[LLM Party] Get Models button clicked");
    state.isProcessing = true;

    try {
      // Remove existing buttons before creating new one
      if (node.widgets) {
        const buttonsToRemove = node.widgets.filter(w => w.type === "button" && w.name === "Get Models");
        for (let i = buttonsToRemove.length - 1; i >= 0; i--) {
          const button = buttonsToRemove[i];
          const idx = node.widgets.indexOf(button);
          if (idx !== -1) {
            node.widgets.splice(idx, 1);
          }
        }
      }

      // Create updating button
      createOrUpdateButton(node, "Updating...");

      // Get widget values
      const baseUrl = getWidgetValue(node, "base_url");
      const apiKey = getWidgetValue(node, "api_key");

      // Send request to our custom endpoint
      const response = await api.fetchApi("/llmparty/refresh_models", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          base_url: baseUrl,
          api_key: apiKey
        })
      });

      // Process the response and update model list
      if (response.ok) {
        const data = await response.json();
        
        // Check if the response contains an error
        if (data.error === "Unauthorized") {
          // API Key error - show alert
          alert("API Response error, please check your key");
          console.error("[LLM Party] API Key error (Unauthorized in response)");

          // Restore the original button
          setTimeout(() => {
            createOrUpdateButton(node, "Get Models");
            state.isProcessing = false;
          }, 200);
          return;
        }
  
        let models = data.models || ["gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"];
  
        // Check if models list is empty
        if (models.length === 0) {
          alert("Can't not get models list");
          console.error("[LLM Party] Empty models list");
  
          // Restore the original button
          setTimeout(() => {
            createOrUpdateButton(node, "Get Models");
            state.isProcessing = false;
          }, 200);
          return;
        }
  
        // Update the model widget options
        const updated = updateComboWidgetOptions(node, "model_name", models);
  
        if (updated) {
          if (node.graph) {
            node.graph.setDirtyCanvas(true, true);
          }
        }
  
        // Restore the original button
        setTimeout(() => {
          createOrUpdateButton(node, "Get Models");
          state.isProcessing = false;
        }, 200);
      } else if (response.status === 401) {
        // API Key error - show alert
        alert("API Response error, please check your key");
        console.error("[LLM Party] API Key error (401)");

        // Restore the original button
        setTimeout(() => {
          createOrUpdateButton(node, "Get Models");
          state.isProcessing = false;
        }, 200);
      } else {
        // Other errors
        console.error(`[LLM Party] API Response error: ${response.status}`);

        // Restore the original button
        setTimeout(() => {
          createOrUpdateButton(node, "Get Models");
          state.isProcessing = false;
        }, 200);
      }
    } catch (error) {
      console.error("[LLM Party] Error updating models:", error);
      alert(`Error: ${error.message}`);

      // Restore the original button even if there's an error
      setTimeout(() => {
        createOrUpdateButton(node, "Get Models");
        state.isProcessing = false;
      }, 200);
    }
  });

  // Force node resize
  node.setSize(node.computeSize());
}

