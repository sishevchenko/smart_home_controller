Telegram controller for smart home

Start: 
	- uvicorn main:app --reload

Logging: 
	linux: tail .\server.log, 
	win32: get-content .\server.log -Wait
