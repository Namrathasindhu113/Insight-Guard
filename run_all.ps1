# PowerShell run_all.ps1
Set-StrictMode -Version Latest
python .\scripts\gen_data.py
Start-Process -NoNewWindow -FilePath python -ArgumentList -NoProfile,-Command,"-c","import uvicorn; uvicorn.run('backend.app:app', host='0.0.0.0', port=8000, reload=True)" 
Start-Sleep -Seconds 3
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/train
streamlit run .\dashboard\app.py
