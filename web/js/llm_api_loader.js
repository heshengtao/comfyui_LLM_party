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
const updateComboWidgetOptions = async (node, widgetName, newOptions) => {
  if (!node) return false;
  try {
    const widget = node.widgets.find(w => w.name === widgetName);
    if (!widget) {
      console.error(`[LLM Party] Widget '${widgetName}' not found`);
      return false;
    }

    console.log(`[LLM Party] === UpdateComboWidgetOptions START ===`);
    console.log(`[LLM Party] Widget name: ${widgetName}`);
    console.log(`[LLM Party] Current widget type: ${widget.type}`);
    console.log(`[LLM Party] Current widget value: ${widget.value}`);
    console.log(`[LLM Party] Current widget options:`, JSON.stringify(widget.options));
    console.log(`[LLM Party] New options count: ${newOptions.length}`);
    console.log(`[LLM Party] New options:`, newOptions);

    const currentValue = widget.value;

    // Method 1: Try converting STRING widget to COMBO type
    if (widget.type === "string" || widget.type === "text") {
      console.log(`[LLM Party] Attempting to convert widget from '${widget.type}' to 'combo'`);

      // Store original properties
      const originalCallback = widget.callback;

      // Change type to combo
      widget.type = "combo";
      widget.options = { values: [...newOptions] };

      console.log(`[LLM Party] After conversion - widget type: ${widget.type}`);
      console.log(`[LLM Party] After conversion - widget options.values:`, widget.options?.values);

      // Try to force LiteGraph to recognize the change
      if (widget.callback) {
        widget.callback(widget.value);
      }
    } else if (widget.type === "combo") {
      console.log(`[LLM Party] Widget is already combo type, updating options`);
      widget.options = widget.options || {};
      widget.options.values = [...newOptions];
    } else {
      console.warn(`[LLM Party] Unknown widget type: ${widget.type}, cannot convert`);
      console.log(`[LLM Party] Available widget types in LiteGraph: "boolean", "number", "string", "combo", "button", "slider"`);
    }

    // Keep current value if it's in the new options, otherwise use first option
    if (newOptions.length > 0) {
      if (!newOptions.includes(currentValue)) {
        widget.value = newOptions[0];
        console.log(`[LLM Party] Setting value to first option: ${newOptions[0]}`);
      } else {
        widget.value = currentValue;
        console.log(`[LLM Party] Keeping current value: ${currentValue}`);
      }
    }

    // Method 2: Force UI refresh using multiple approaches
    console.log(`[LLM Party] Triggering UI refresh...`);

    // Approach 1: Mark canvas as dirty
    node.setDirtyCanvas(true, true);
    if (node.graph) {
      node.graph.setDirtyCanvas(true, true);
    }

    // Approach 2: Trigger widget change event
    if (app.canvas) {
      app.canvas.dirty = true;
    }

    // Approach 3: Force node resize
    const oldSize = node.size;
    node.size = [oldSize[0] + 1, oldSize[1]];
    setTimeout(() => {
      node.size = oldSize;
      node.setDirtyCanvas(true, true);
    }, 10);

    // Multiple refresh attempts
    for (let i = 50; i <= 200; i += 50) {
      setTimeout(() => {
        console.log(`[LLM Party] Refresh attempt at ${i}ms`);
        node.setDirtyCanvas(true, true);
        if (node.graph) {
          node.graph.setDirtyCanvas(true, true);
        }
        if (app.canvas) {
          app.canvas.dirty = true;
        }
      }, i);
    }

    // Final status log
    setTimeout(() => {
      console.log(`[LLM Party] === Final Status ===`);
      console.log(`[LLM Party] Final widget type: ${widget.type}`);
      console.log(`[LLM Party] Final widget options.values count: ${widget.options?.values?.length || 0}`);
      console.log(`[LLM Party] Final widget value: ${widget.value}`);
      console.log(`[LLM Party] === UpdateComboWidgetOptions END ===`);
    }, 300);

    console.log(`[LLM Party] Widget update completed, type: ${widget.type}, options: ${widget.options?.values?.length || 0} items`);
    return true;
  } catch (e) {
    console.error(`[LLM Party] Error updating widget options:`, e);
    console.error(`[LLM Party] Stack trace:`, e.stack);
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
      let baseUrl = getWidgetValue(node, "base_url");
      let apiKey = getWidgetValue(node, "api_key");

      // Fallback values
      baseUrl = baseUrl || "https://api.openai.com/v1";
      apiKey = apiKey || "";

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

