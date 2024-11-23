@echo off

set "python_exec=..\..\..\python_embeded\python.exe"

echo Installing ONNX Runtime GPU...

if exist "%python_exec%" (
    echo Installing with ComfyUI Portable
    "%python_exec%" -m pip uninstall -y onnxruntime
    "%python_exec%" -m pip uninstall -y onnxruntime-gpu
    "%python_exec%" -m pip install onnxruntime-gpu
) else (
    echo Installing with system Python
    pip uninstall -y onnxruntime
    pip uninstall -y onnxruntime-gpu
    pip install onnxruntime-gpu
)

pause
