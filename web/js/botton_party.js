import { app } from "../../scripts/app.js";

class LLMPartyExtension {
    constructor() {
        this.container = null;
        this.apiButton = null;
        this.aboutButton = null;
        this.fastApiButton = null;
        this.streamlitButton = null;
        this.workflowButton = null;
        this.toggleButton = null;
        this.apiModal = null;
        this.aboutModal = null;
        this.workflowModal = null;
        this.isExpanded = true;
        this.EXPANDED_WIDTH = '150px'; // 新增：定义展开时的宽度

        // 从 localStorage 加载保存的位置
        const savedPosition = JSON.parse(localStorage.getItem('LLMPartyPosition')) || {};
        console.log('Loaded saved position:', savedPosition);

        this.createContainer(savedPosition);
        this.createAPIModal();
        this.createAboutModal();
        this.createWorkflowModal();

        this.makeDraggable(this.container);

        // 在页面加载完成后应用保存的位置
        window.addEventListener('load', () => this.applyPosition(savedPosition));
    }

    createContainer(savedPosition) {
        this.container = document.createElement('div');
        
        // 计算初始位置，优先使用保存的位置
        const windowWidth = window.innerWidth;
        const windowHeight = window.innerHeight;
        const initialLeft = savedPosition.left !== undefined ? savedPosition.left : (windowWidth / 2) - 100;
        const initialTop = savedPosition.top !== undefined ? savedPosition.top : 0;

        this.container.style.cssText = `
            position: fixed;
            top: ${initialTop}px;
            left: ${initialLeft}px;
            height: 30px;
            background-color: #1e1e1e;
            border: 1px solid #444;
            border-radius: 5px;
            display: flex;
            align-items: center;
            z-index: 9999;
            transition: width 0.3s ease-in-out;
        `;

        const dragHandle = document.createElement('div');
        dragHandle.style.cssText = `
            width: 20px;
            height: 100%;
            background-color: #2c2c2c;
            cursor: move;
            display: flex;
            align-items: center;
            justify-content: center;
        `;
        dragHandle.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="1" />
                <circle cx="12" cy="5" r="1" />
                <circle cx="12" cy="19" r="1" />
            </svg>
        `;

        const buttonWrapper = document.createElement('div');
        buttonWrapper.style.cssText = `
            display: flex;
            height: 100%;
            overflow: hidden;
            transition: width 0.3s ease-in-out;
            width: ${this.EXPANDED_WIDTH}; // 使用常量设置初始宽度
        `;

        this.apiButton = this.createButton('API-key', `
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4" />
            </svg>
        `, () => this.showAPIModal());

        this.fastApiButton = this.createButton('FastAPI', `
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
                <polyline points="22 4 12 14.01 9 11.01" />
            </svg>
        `, () => this.sendFastApiRequest());

        this.streamlitButton = this.createButton('Streamlit', `
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                <line x1="3" y1="9" x2="21" y2="9"></line>
                <line x1="9" y1="21" x2="9" y2="9"></line>
            </svg>
        `, () => this.sendStreamlitRequest());

        this.aboutButton = this.createButton('About', `
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22" />
            </svg>
        `, () => this.showAboutModal());

        this.toggleButton = this.createButton('Close', `
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="15 18 9 12 15 6"></polyline>
            </svg>
        `, () => this.toggleExpansion());
        this.toggleButton.style.width = '20px';
        this.toggleButton.style.borderRight = 'none';

        this.workflowButton = this.createButton('Workflow', `
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M3 3v18h18"/>
                <path d="M18.7 8l-5.1 5.2-2.8-2.7L7 14.3"/>
            </svg>
        `, () => this.showWorkflowModal());

        buttonWrapper.appendChild(this.apiButton);
        buttonWrapper.appendChild(this.fastApiButton);
        buttonWrapper.appendChild(this.streamlitButton);
        buttonWrapper.appendChild(this.workflowButton);
        buttonWrapper.appendChild(this.aboutButton);

        this.container.appendChild(dragHandle);
        this.container.appendChild(buttonWrapper);
        this.container.appendChild(this.toggleButton);
        document.body.appendChild(this.container);
    }

    createButton(title, svgContent, onClick) {
        const button = document.createElement('button');
        button.innerHTML = svgContent;
        button.title = title;
        button.style.cssText = `
            width: 30px;
            height: 100%;
            background-color: #2c2c2c;
            color: white;
            border: none;
            border-right: 1px solid #444;
            padding: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
        `;
        button.onclick = onClick;
        return button;
    }

    toggleExpansion() {
        this.isExpanded = !this.isExpanded;
        const buttonWrapper = this.container.querySelector('div:nth-child(2)');
        if (this.isExpanded) {
            buttonWrapper.style.width = this.EXPANDED_WIDTH; // 使用常量设置展开宽度
            this.toggleButton.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="15 18 9 12 15 6"></polyline>
                </svg>
            `;
            this.toggleButton.title = 'Close';
        } else {
            buttonWrapper.style.width = '0px';
            this.toggleButton.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="9 18 15 12 9 6"></polyline>
                </svg>
            `;
            this.toggleButton.title = 'Expand';
        }

        // 如果在右边界，保持吸附
        const windowWidth = window.innerWidth;
        const elementWidth = this.container.offsetWidth;
        const currentLeft = parseInt(this.container.style.left);
        if (currentLeft + elementWidth > windowWidth - 5) {
            this.container.style.left = (windowWidth - this.container.querySelector('div:first-child').offsetWidth - this.toggleButton.offsetWidth) + "px";
        }
    }


    // ... 其余方法保持不变 ...
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
            padding: 20px;
            border: 1px solid #888;
            width: 300px;
            border-radius: 5px;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
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
            padding: 20px;
            border: 1px solid #888;
            width: 60%;
            max-width: 600px;
            border-radius: 5px;
            color: white;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
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
            <p>注意！本项目是基于AGPL协议开源的，请遵守AGPL协议，以避免不必要的法律问题！谢谢您的合作！如果您需要可以闭源商用的版本，请邮箱联系hst97@qq.com</p>
            <p>Attention! This project is open source based on the AGPL agreement, please abide by the AGPL agreement to avoid unnecessary legal problems! Thank you for your cooperation! If you need a closed-source commercial version, please contact hst97@qq.com</p>
            <p>github: <a href="https://github.com/heshengtao/comfyui_LLM_party" target="_blank" style="color: #4CAF50;">heshengtao/comfyui_LLM_party</a></p>
            <p>bilibili: <a href="https://space.bilibili.com/26978344?spm_id_from=333.1007.0.0" target="_blank" style="color: #4CAF50;">@派酱llm-party</a></p>
            <p>youtube: <a href="https://www.youtube.com/@comfyui-LLM-party" target="_blank" style="color: #4CAF50;">@comfyui-LLM-party</a></p>
            <p>QQ: <a href="https://github.com/heshengtao/comfyui_LLM_party/blob/main/img/Q%E7%BE%A4.jpg" target="_blank" style="color: #4CAF50;">931057213</a></p>
            <p>feishu: <a href="https://dcnsxxvm4zeq.feishu.cn/wiki/IyUowXNj9iH0vzk68cpcLnZXnYf?fromScene=spaceOverview" target="_blank" style="color: #4CAF50;">use document</a></p>
        `;

        modalContent.appendChild(closeBtn);
        modalContent.appendChild(title);
        modalContent.appendChild(content);

        this.aboutModal.appendChild(modalContent);
        document.body.appendChild(this.aboutModal);
    }

    showAPIModal() {
        this.apiModal.style.display = 'block';
        this.centerModalContent(this.apiModal);
    }

    hideAPIModal() {
        this.apiModal.style.display = 'none';
    }

    showAboutModal() {
        this.aboutModal.style.display = 'block';
        this.centerModalContent(this.aboutModal);
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

    async sendFastApiRequest() {
        const endpoint = '/party/fastapi';
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({})
            });

            if (response.ok) {
                const result = await response.json();
                console.log('FastAPI请求成功:', result);
                alert('The FastAPI request was sent and successfully processed!');
            } else {
                const errorMessage = await response.text();
                console.error('FastAPI request failed:', response.status, errorMessage);
                alert(`FastAPI request failed: ${errorMessage}`);
            }
        } catch (error) {
            console.error('FastAPI request failed:', error);
            alert(`Error occurred: ${error.message}`);
        }
    }

    async sendStreamlitRequest() {
        const endpoint = '/party/streamlit';
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({})
            });

            if (response.ok) {
                const result = await response.json();
                console.log('Streamlit请求成功:', result);
                alert('The Streamlit app is launched! Please check it in a new window.');
            } else {
                const errorMessage = await response.text();
                console.error('Streamlit request failed:', response.status, errorMessage);
                alert(`Streamlit request failed: ${errorMessage}`);
            }
        } catch (error) {
            console.error('Streamlit request failed:', error);
            alert(`Error occurred: ${error.message}`);
        }
    }

makeDraggable(element) {
    let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
    const dragHandle = element.querySelector('div');
    dragHandle.onmousedown = dragMouseDown;

    function dragMouseDown(e) {
        e = e || window.event;
        e.preventDefault();
        pos3 = e.clientX;
        pos4 = e.clientY;
        document.onmouseup = closeDragElement;
        document.onmousemove = elementDrag;
    }

    const elementDrag = (e) => {
        e = e || window.event;
        e.preventDefault();
        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;

        let newTop = element.offsetTop - pos2;
        let newLeft = element.offsetLeft - pos1;

        const windowWidth = window.innerWidth;
        const windowHeight = window.innerHeight;
        const elementWidth = element.offsetWidth;
        const elementHeight = element.offsetHeight;

        // 上下边界吸附
        if (newTop < 5) newTop = 0;
        if (newTop > windowHeight - elementHeight - 5) newTop = windowHeight - elementHeight;

        // 左边界吸附并触发Close
        if (newLeft < 5) {
            newLeft = 0;
            if (this.isExpanded) {
                this.toggleExpansion();
            }
        }

        // 右边界吸附并触发Close
        if (newLeft > windowWidth - elementWidth - 5) {
            if (this.isExpanded) {
                this.toggleExpansion();
            }
            newLeft = windowWidth - this.container.querySelector('div:first-child').offsetWidth - this.toggleButton.offsetWidth;
        }

        // 更新位置
        element.style.top = newTop + "px";
        element.style.left = newLeft + "px";

        // 保存位置到 localStorage
        localStorage.setItem('LLMPartyPosition', JSON.stringify({ top: newTop, left: newLeft }));
        console.log('Position saved:', { top: newTop, left: newLeft });
    }

    function closeDragElement() {
        document.onmouseup = null;
        document.onmousemove = null;
    }
    }

    createWorkflowModal() {
        this.workflowModal = document.createElement('div');
        this.workflowModal.style.cssText = `
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
            padding: 20px;
            border: 1px solid #888;
            width: 300px;
            border-radius: 5px;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
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
        closeBtn.onclick = () => this.hideWorkflowModal();

        const title = document.createElement('h2');
        title.textContent = 'Select Workflow';
        title.style.color = 'white';

        const select = document.createElement('select');
        select.id = 'workflowSelect';
        select.style.cssText = `
            width: 100%;
            padding: 5px;
            margin: 5px 0;
            box-sizing: border-box;
            background-color: #3c3c3c;
            color: white;
            border: 1px solid #555;
        `;

        const loadButton = document.createElement('button');
        loadButton.textContent = 'load workflow';
        loadButton.style.cssText = `
            background-color: #4CAF50;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 3px;
            cursor: pointer;
            width: 100%;
            margin-top: 10px;
        `;
        loadButton.onclick = () => this.loadSelectedWorkflow();

        modalContent.appendChild(closeBtn);
        modalContent.appendChild(title);
        modalContent.appendChild(select);
        modalContent.appendChild(loadButton);

        this.workflowModal.appendChild(modalContent);
        document.body.appendChild(this.workflowModal);

        // 加载工作流列表
        this.loadWorkflowList();
    }

    showWorkflowModal() {
        this.workflowModal.style.display = 'block';
        this.centerModalContent(this.workflowModal);
    }

    hideWorkflowModal() {
        this.workflowModal.style.display = 'none';
    }

    centerModalContent(modal) {
        const content = modal.querySelector('div');
        const windowHeight = window.innerHeight;
        const contentHeight = content.offsetHeight;
        
        if (contentHeight > windowHeight) {
            content.style.top = '0';
            content.style.transform = 'translateX(-50%)';
        } else {
            content.style.top = '50%';
            content.style.transform = 'translate(-50%, -50%)';
        }
    }

    async loadWorkflowList() {
        const select = document.getElementById('workflowSelect');
        try {
            const response = await fetch('/party/workflow_list');
            if (response.ok) {
                const workflows = await response.json();
                select.innerHTML = '';
                workflows.forEach(workflow => {
                    const option = document.createElement('option');
                    option.value = workflow;
                    option.textContent = workflow;
                    select.appendChild(option);
                });
            } else {
                console.error('Failed to load workflow list');
            }
        } catch (error) {
            console.error('Error loading workflow list:', error);
        }
    }

    async loadSelectedWorkflow() {
        const select = document.getElementById('workflowSelect');
        const selectedWorkflow = select.value;
        if (selectedWorkflow) {
            try {
                const response = await fetch('/party/load_workflow', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ workflow: selectedWorkflow })
                });
                if (response.ok) {
                    const workflow = await response.json();
                    app.loadGraphData(workflow);
                    this.hideWorkflowModal();
                    alert('Workflow loaded successfully!');
                } else {
                    alert('Failed to load workflow');
                }
            } catch (error) {
                console.error('Error loading workflow:', error);
                alert('An error occurred while loading the workflow');
            }
        }
    }

    applyPosition(savedPosition) {
        if (savedPosition.top !== undefined && savedPosition.left !== undefined) {
            this.container.style.top = `${savedPosition.top}px`;
            this.container.style.left = `${savedPosition.left}px`;
            console.log('Applied saved position:', savedPosition);
        }
    }
}

// 注册扩展
app.registerExtension({
    name: "comfy.LLMPartyExtension",
    setup() {
        new LLMPartyExtension();
    },
});
