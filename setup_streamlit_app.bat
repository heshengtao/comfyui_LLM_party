@echo off
echo Starting Streamlit app...
..\..\..\python_embeded\python.exe -m streamlit run %~dp0api.py
pause
