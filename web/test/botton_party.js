import { app } from "../../scripts/app.js";

class LLMPartyExtension {
    constructor() {
        this.container = null;
        this.apiButton = null;
        this.aboutButton = null;
        this.apiModal = null;
        this.aboutModal = null;

        this.createContainer();
        this.createAPIModal();
        this.createAboutModal();

        this.makeDraggable(this.container);
    }

    createContainer() {
        this.container = document.createElement('div');
        this.container.style.cssText = `
            position: fixed;
            top: 60px;
            left: 20px;
            width: 180px;
            height: 30px;
            background-color: #1e1e1e;
            border: 1px solid #444;
            border-radius: 5px;
            display: flex;
            align-items: center;
            z-index: 1000;
            cursor: move;
        `;

        const buttonWrapper = document.createElement('div');
        buttonWrapper.style.cssText = `
            display: flex;
            width: 100%;
            height: 100%;
        `;

        this.apiButton = document.createElement('button');
        this.apiButton.textContent = 'API Key';
        this.apiButton.style.cssText = `
            flex: 1;
            height: 100%;
            background-color: #2c2c2c;
            color: white;
            border: none;
            border-right: 1px solid #444;
            padding: 0;
            font-size: 16px;
            cursor: pointer;
        `;
        this.apiButton.onclick = () => this.showAPIModal();

        this.aboutButton = document.createElement('button');
        this.aboutButton.textContent = 'About Us';
        this.aboutButton.style.cssText = `
            flex: 1;
            height: 100%;
            background-color: #2c2c2c;
            color: white;
            border: none;
            padding: 0;
            font-size: 16px;
            cursor: pointer;
        `;
        this.aboutButton.onclick = () => this.showAboutModal();

        buttonWrapper.appendChild(this.apiButton);
        buttonWrapper.appendChild(this.aboutButton);

        this.container.appendChild(buttonWrapper);
        document.body.appendChild(this.container);
    }

    createAPIModal() {
        this.apiModal = document.createElement('div');
        this.apiModal.style.cssText = `
            display: none;
            position: fixed;
            z-index: 1001;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgba(0,0,0,0.4);
        `;

        const modalContent = document.createElement('div');
        modalContent.style.cssText = `
            background-color: #2c2c2c;
            margin: 15% auto;
            padding: 20px;
            border: 1px solid #888;
            width: 300px;
            border-radius: 5px;
        `;

        const closeBtn = document.createElement('span');
        closeBtn.innerHTML = '&times;';
        closeBtn.style.cssText = `
            color: #aaa;
            float: right;
            font-size: 28px;
            font-weight: bold;
            cursor: pointer;
        `;
        closeBtn.onclick = () => this.hideAPIModal();

        const title = document.createElement('h2');
        title.textContent = 'Set API Key';
        title.style.color = 'white';

        const form = document.createElement('form');
        form.onsubmit = (e) => this.submitApiKey(e);

        const baseUrlLabel = document.createElement('label');
        baseUrlLabel.textContent = 'Base URL:';
        baseUrlLabel.style.color = 'white';
        const baseUrlInput = document.createElement('input');
        baseUrlInput.type = 'text';
        baseUrlInput.id = 'baseUrl';
        baseUrlInput.value = 'https://api.openai.com/v1/';
        baseUrlInput.style.cssText = `
            width: 100%;
            padding: 5px;
            margin: 5px 0;
            box-sizing: border-box;
            background-color: #3c3c3c;
            color: white;
            border: 1px solid #555;
        `;

        const apiKeyLabel = document.createElement('label');
        apiKeyLabel.textContent = 'API Key:';
        apiKeyLabel.style.color = 'white';
        const apiKeyInput = document.createElement('input');
        apiKeyInput.type = 'password';
        apiKeyInput.id = 'apiKey';
        apiKeyInput.style.cssText = `
            width: 100%;
            padding: 5px;
            margin: 5px 0;
            box-sizing: border-box;
            background-color: #3c3c3c;
            color: white;
            border: 1px solid #555;
        `;

        const submitButton = document.createElement('button');
        submitButton.type = 'submit';
        submitButton.textContent = 'Set API Key';
        submitButton.style.cssText = `
            background-color: #4CAF50;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 3px;
            cursor: pointer;
            width: 100%;
            margin-top: 10px;
        `;

        form.appendChild(baseUrlLabel);
        form.appendChild(baseUrlInput);
        form.appendChild(apiKeyLabel);
        form.appendChild(apiKeyInput);
        form.appendChild(submitButton);

        modalContent.appendChild(closeBtn);
        modalContent.appendChild(title);
        modalContent.appendChild(form);

        this.apiModal.appendChild(modalContent);
        document.body.appendChild(this.apiModal);
    }

    createAboutModal() {
        this.aboutModal = document.createElement('div');
        this.aboutModal.style.cssText = `
            display: none;
            position: fixed;
            z-index: 1001;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgba(0,0,0,0.4);
        `;

        const modalContent = document.createElement('div');
        modalContent.style.cssText = `
            background-color: #2c2c2c;
            margin: 15% auto;
            padding: 20px;
            border: 1px solid #888;
            width: 60%;
            max-width: 600px;
            border-radius: 5px;
            color: white;
        `;

        const closeBtn = document.createElement('span');
        closeBtn.innerHTML = '&times;';
        closeBtn.style.cssText = `
            color: #aaa;
            float: right;
            font-size: 28px;
            font-weight: bold;
            cursor: pointer;
        `;
        closeBtn.onclick = () => this.hideAboutModal();

        const title = document.createElement('h2');
        title.textContent = 'ComfyUI LLM Party';

        const content = document.createElement('div');
        content.innerHTML = `
            <p>项目发起人：heshengtao</p>
            <p>项目地址: <a href="https://github.com/heshengtao/comfyui_LLM_party" target="_blank" style="color: #4CAF50;">https://github.com/heshengtao/comfyui_LLM_party</a></p>
            <p>项目频道: <a href="https://space.bilibili.com/26978344?spm_id_from=333.1007.0.0" target="_blank" style="color: #4CAF50;">https://space.bilibili.com/26978344</a></p>
            <p>ComfyUI LLM Party是一个致力于在ComfyUI的开源生态中打造一个功能强大的LLM Agent生态，将LLM与图像生成领域之间的gap打通，同时将ComfyUI做成一个可万物互联的移动接口，零代码实现个人AI Agent的创造，门槛低，自由度强。</p>
        `;

        modalContent.appendChild(closeBtn);
        modalContent.appendChild(title);
        modalContent.appendChild(content);

        this.aboutModal.appendChild(modalContent);
        document.body.appendChild(this.aboutModal);
    }

    showAPIModal() {
        this.apiModal.style.display = 'block';
    }

    hideAPIModal() {
        this.apiModal.style.display = 'none';
    }

    showAboutModal() {
        this.aboutModal.style.display = 'block';
    }

    hideAboutModal() {
        this.aboutModal.style.display = 'none';
    }

    async submitApiKey(e) {
        e.preventDefault();
        const baseUrl = document.getElementById('baseUrl').value;
        const apiKey = document.getElementById('apiKey').value;
        const endpoint = '/party/update_config';  // New endpoint for updating config
    
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    openai_api_key: apiKey,
                    base_url: baseUrl
                })
            });
    
            if (response.ok) {
                const result = await response.json();
                alert('API Key and Base URL updated successfully!');
                this.hideAPIModal();
            } else {
                const errorMessage = await response.text();
                console.error('Server responded with an error:', response.status, errorMessage);
                alert(`Failed to update API Key and Base URL: ${errorMessage}`);
            }
        } catch (error) {
            console.error('Fetch error:', error);
            alert(`An error occurred: ${error.message}`);
        }
    }

    makeDraggable(element) {
        let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
        element.onmousedown = dragMouseDown;

        function dragMouseDown(e) {
            e = e || window.event;
            e.preventDefault();
            pos3 = e.clientX;
            pos4 = e.clientY;
            document.onmouseup = closeDragElement;
            document.onmousemove = elementDrag;
        }

        function elementDrag(e) {
            e = e || window.event;
            e.preventDefault();
            pos1 = pos3 - e.clientX;
            pos2 = pos4 - e.clientY;
            pos3 = e.clientX;
            pos4 = e.clientY;
            element.style.top = (element.offsetTop - pos2) + "px";
            element.style.left = (element.offsetLeft - pos1) + "px";
        }

        function closeDragElement() {
            document.onmouseup = null;
            document.onmousemove = null;
        }
    }
}

// Register the extension
app.registerExtension({
    name: "comfy.LLMPartyExtension",
    setup() {
        new LLMPartyExtension();
    },
});