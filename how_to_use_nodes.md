# **Node Usage Instructions**

## Models

### LLM_API Node
1. Large model nodes can customize model name, temperature, API_KEY, base_url, currently only supports openai type API interface calls.
2. You can directly input system prompts and user prompts on the node, or right-click to convert these two widgets into node inputs, accepting string type inputs.
3. Large model nodes can also accept outputs from tool nodes through the tools interface and accept string inputs from the file_content interface, which will be used as the model's knowledge base, searching for related content to input into the model based on word vector similarity.
4. The is_memory of the large model node can determine whether the large model has memory. You can change is_memory to disable, then run, at which time the model will clear the previous conversation records, then switch back to enable, and the model will retain your conversation records in subsequent runs.
5. You can view the model's reply in this round of conversation through assistant_response, or view the history of multiple rounds of conversation through history.
6. Even if the external parameters do not change, the large model node will always run, because the large model always has different answers to the same question.
7. is_tools_in_sys_prompt determines whether the information of tools will be input into the system prompts.
8. is_locked can lock the results of the previous round of conversation, allowing the large model to directly return the answer from the previous round of conversation.
9. main_brain determines whether the large model is the model that interfaces with the user. If disabled, the LLM node can serve as a tool for another LLM node.
10. imgbb_api_key can input imgbb's pi_key, and LLM will adapt to GPT4's visual capabilities.

### LLM_Local Node
1. Currently supports GLM/Llama/Qwen, but only GLM's tool calling is perfectly adapted, the other two require a large parameter version to call tools normally.
2. is_reload determines whether to unload the local model after the node runs. It is disabled by default to prevent reloading the large model and increasing running time. When the video memory cannot support running LLM and SD at the same time, it can be enabled.
3. Input the model's project folder into model_path and tokenizer_path, compatible with all models that can be compatible with transformer.
4. Other parameters are consistent with the LLM_API node.

### Embedding Model
1. The file_content node can input a string, which will be used as the input to the word embedding model. The model will search on this string and return the most relevant text content based on the question.
2. chuck_size is the size of each text block when the text is split, the default is 200, chuck_overlap is the overlap size between each text block when the text is split, the default is 50.
3. Input embedding_path, and the embedding model in this folder will be called.

## Loaders

### Load_File Node
1. The path to read the file is in comfyui_LLM_party/file, you can put the file you want to read in this path, and then fill in the file name in this node.
2. You can choose absolute path input, in which case path can accept an absolute path.
3. The output is a string that contains all the text information in the file.
4. The adapted file formats are: ".docx", ".txt", ".pdf", ".xlsx", ".csv", ".py", ".js", ".java", ".c", ".cpp", ".html", ".css", ".sql", ".r", ".swift"

### Load_Folder Node
1. folder_path can accept an absolute path of a folder, and this node will automatically read all the files in the folder.
2. The output is a string that contains all the text information in the folder.
3. The adapted file formats are: ".docx", ".txt", ".pdf", ".xlsx", ".csv", ".py", ".js", ".java", ".c", ".cpp", ".html", ".css", ".sql", ".r", ".swift"

### Load_url_content Node
1. Can convert all web page content in a url into an md format output.
2. The output is a string that contains all the text information on the web page.

### Load_Wikipedia Node
1. Can return all content related to the question in Wikipedia.

### Load_Persona Node
1. Can return a preset persona persona, which can be used as the system_prompt_input of the large model, allowing the large model to have the personality of the persona.
2. The persona folder contains the persona of the image prompt assistant and DAN. You can add more personas to this folder for your use.

## Persona

### Classifier persona and Super Large Classifier persona Nodes
1. You can use this persona node as the system_prompt_input of the LLM node, allowing the large model to have the personality of the persona.
2. LLM will classify user_prompt according to the categories described on the classifier persona node.
3. Can be used in conjunction with classifier functions to output different categories of text to different workflows.

### Custom persona
1. prompt is the system_prompt_input that will be input into the LLM node, which can contain some variables, such as: "You are an intelligent customer service about {app}, you need to generate content related to {text}", where {text} will automatically be filled with the user_prompt received by LLM.
2. prompt_template contains the corresponding rules for the variables in the prompt, generally in json format, which can be filled in as follows: {"app":"chatgpt"}, at this time, {app} in the prompt will be automatically replaced with chatgpt.

## Functions

### Classifier Function and Super Large Classifier Function Nodes
1. Can split the string processed by the LLM with a classifier persona into multiple strings, which can be used in conjunction with string logic to control the execution of the corresponding workflow.

### String Logic
1. option contains the following options: "A contain B", "A not contain B", "A relate to B", "A not relate to B", "A equal B", "A not equal B", "A is null", "A is not null" for selection.
2. When the condition is true, if will output A string, else will output an empty string, is_true will output true, is_false will output false, otherwise else will output A string, if will output an empty string, is_true will output false, is_false will output true.

### Text Display Function
1. Can directly display the input string on the comfyui interface.

## Tools

### Classifier Node
1. Input a string, which will be used as the user_prompt of the large model, allowing the large model to have the personality of the persona.

## Combinations

### File Combination, Super Large File Combination Nodes
1. Used to combine multiple strings into one string.
2. These combination nodes can be nested.

### Tool Combination, Super Large Tool Combination Nodes
1. Used to combine multiple tool nodes into one tool node, then input to the large model.
2. These combination nodes can be nested.

## Tools

### Time_Tool, Weather_Tool, AccuWeather_Tool Nodes
1. Used for querying time and weather. The time tool node can change the default time zone for queries, and the weather tool node will also add an option to change the default region in the future (this free weather tool is limited to searching for weather in China).
2. The AccuWeather tool node requires an AccuWeather API key to query global weather.

### Google_Tool Node
1. You can use this node by entering your Google API key and CSE ID.
2. This node will return the top 10 URLs and summaries from Google search. You can ask the model to paginate to see later search results.

### check_web_Tool Node
1. You can enter the URL you want to search into this node as the default URL for the model's search. This node will convert all content of this webpage into Markdown format and return it to the model.
2. Since requests are not omnipotent, some URLs may not allow crawling, and this project does not provide malicious crawler code.
3. You can input an embedding_path, which will call the word embedding model in this folder. The tool will split the webpage content according to chuck_size and chuck_overlap, returning only the text information related to the user's question.
4. If there is no embedding_path, it will return all content of the webpage.

### Embeddings_Tool Node
1. The specific function is the same as the word embedding model node, but this node is a tool for LLM, which can be called when the model thinks it needs to query the knowledge base, using the file_content input into this tool.

### Interpreter Node
1. Allows the large model to generate Python code, run it automatically, and obtain the results of the code execution.
2. Currently, only supports Python code.

### Omnipotent_Interpreter Node
1. Allows the large model to do anything. The large model will download the required third-party libraries in a virtual environment and then execute the generated code.
2. Please use this tool carefully, as the large model will gain the ability to control your computer to do anything!

### API_Tool Node
1. Fill in the URL that needs to be accessed.
2. The first text input box is for entering the function of this API tool, for example: a tool for checking the weather.
3. The second text input box is for entering the parameters of this API tool, for example: the parameters for the weather-checking tool are: {"city":"beijing"}

### Wikipedia_Tool Node
1. Allows the large model to query content related to Wikipedia.
2. You can input an embedding_path, which will call the word embedding model in this folder. The tool will split the Wikipedia content according to chuck_size and chuck_overlap, returning only the text information related to the user's question.
3. If there is no embedding_path, it will return the first 1000 characters related to Wikipedia.

### arXiv_Tool Node
1. Allows the large model to query relevant research papers on arXiv.
2. The default search is for the research direction in the query.

## Workflow Nodes

### Start_Workflow and End_Workflow Nodes
1. You can use these two nodes to define the start and end points of the workflow, placing your workflow in the workflow subfolder of this project folder.
2. Click setup_streamlit_app.bat in the project folder, and in the Streamlit interface, click settings and replace it with your workflow.
3. This way, you quickly build an AI application with Streamlit as the frontend.

### Start_Dialog Node and End_Dialog Node
1. Both of these nodes have a dialog_id, connecting the dialog_id to make them a dialogue archive point. When you need to loop-connect two large models, although it cannot be achieved in comfyui, you can save the output of the latter model locally, and then pass it to the previous model the next time it runs. You can call comfyui with the comfyui API in other frontends, and as long as you keep calling, you can see the infinite self-dialogue of the two models.
2. The start dialogue node has an interface for starting a dialogue, which can serve as a prompt given by the user at the start of a dialogue, guiding the large model to discuss within the topic given by the user.

### Workflow_transfer Node
1. Allows your workflow to call other workflows!
2. Add start workflow and end workflow nodes to the beginning and end of the workflow you want to embed, and save this workflow as an API in the workflow_api folder of the comfyui_LLM_party project.
3. Open another workflow, use the workflow switch node in this workflow, select the workflow you want to embed, and it's done.
4. The first time you use the workflow switch node, another 8189 port will be opened, please do not close this new console.

## Image

### Party Versions of CLIP Text Encoder, Sampler, Decoder
1. These nodes have been modified by me so that they will not error out when input is missing, but will be bypassed instead. I think this feature is very important, but I don't know why comfyui doesn't write this feature. This feature can control which part of the workflow is executed by controlling whether there is input to the workflow.
