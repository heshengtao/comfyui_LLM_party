document.addEventListener('DOMContentLoaded', () => {
  const baseUrlInput = document.getElementById('base-url');
  const apiKeyInput = document.getElementById('api-key');
  const modelNameInput = document.getElementById('model-name');
  const systemPromptInput = document.getElementById('system-prompt');
  const userInput = document.getElementById('user-input');
  const sendInputButton = document.getElementById('send-input');
  const saveSettingsButton = document.getElementById('save-settings');
  const responseContainer = document.getElementById('response-container');
  const copyResponseButton = document.getElementById('copy-response'); // 新的复制按钮
  const clearResponseButton = document.getElementById('clear-response'); // 新的清除按钮

  // Load saved settings
  chrome.storage.local.get(['baseUrl', 'apiKey', 'modelName', 'systemPrompt', 'markdownResponse', 'isThinking'], (data) => {
    baseUrlInput.value = data.baseUrl || 'http://127.0.0.1:8187/v1';
    apiKeyInput.value = data.apiKey || 'party';
    modelNameInput.value = data.modelName || 'X';
    systemPromptInput.value = data.systemPrompt || '';
    responseContainer.innerHTML = marked.parse(data.markdownResponse || 'No response yet.');
    sendInputButton.disabled = data.isThinking || false;
  });

  // Save settings
  saveSettingsButton.addEventListener('click', () => {
    const baseUrl = baseUrlInput.value;
    const apiKey = apiKeyInput.value;
    const modelName = modelNameInput.value;
    const systemPrompt = systemPromptInput.value;

    chrome.storage.local.set({ baseUrl, apiKey, modelName, systemPrompt }, () => {
      alert('Settings saved!');
    });
  });

  // Send user input
  sendInputButton.addEventListener('click', () => {
    const baseUrl = baseUrlInput.value;
    const apiKey = apiKeyInput.value;
    const modelName = modelNameInput.value;
    const systemPrompt = systemPromptInput.value;
    const userText = userInput.value;

    // 禁用按钮并显示 "Thinking..."
    sendInputButton.disabled = true;
    responseContainer.innerHTML = "Thinking...";

    fetch(`${baseUrl}/chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`
      },
      body: JSON.stringify({
        model: modelName,
        messages: [
          { role: "system", content: systemPrompt },
          { role: "user", content: userText }
        ]
      })
    })
    .then(response => response.json())
    .then(data => {
      const markdownResponse = data.choices[0].message.content;
      chrome.storage.local.set({ markdownResponse });
      responseContainer.innerHTML = marked.parse(markdownResponse);
      enableInputButton(); // 恢复按钮可用状态
    })
    .catch(error => {
      responseContainer.innerHTML = "Error: Unable to fetch response.";
      enableInputButton(); // 恢复按钮可用状态
    });
  });

  // Copy response to clipboard
  copyResponseButton.addEventListener('click', () => {
    const textToCopy = responseContainer.innerText.trim(); // 使用 trim() 去除前后多余的空格
    navigator.clipboard.writeText(textToCopy).then(() => {
      alert('Response copied to clipboard!');
    });
  });

  // Clear response
  clearResponseButton.addEventListener('click', () => {
    responseContainer.innerHTML = '';
    chrome.storage.local.set({ markdownResponse: 'No response yet.' });
  });

  // 监听 storage 变化，刷新输出框内容
  chrome.storage.onChanged.addListener((changes, namespace) => {
    if (changes.markdownResponse) {
      responseContainer.innerHTML = marked.parse(changes.markdownResponse.newValue);
    }
  });

  // 监听来自 background.js 的消息
  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "updateUI") {
      chrome.storage.local.get(['markdownResponse', 'isThinking'], (data) => {
        responseContainer.innerHTML = marked.parse(data.markdownResponse || 'No response yet.');
        sendInputButton.disabled = data.isThinking || false;
      });
    }
  });

  // 恢复按钮可用状态的函数
  function enableInputButton() {
    sendInputButton.disabled = false;
  }
});
