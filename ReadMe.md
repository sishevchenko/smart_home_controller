***
Author: sishevchenko  
GitHub: https://github.com/sishevchenko  
Telegram: @s_i_shevchenko  
***

# en_EN
Telegram controller for smart home
...

# ru_RU
Телеграм контроллер для управления умным домом  
Проект реализован на базе FastAPI, aiogram и sqlite3  
Целью данного проекта является изучение возможности интеграции телеграм бота в структуру приложения FastAPI  


## Start:
For start use this commands:  

`uvicorn main:app OPTIONAL[--reload]`  
`docker build . -t smart_home_controller:latest`  
`docker rum smart_home_controller`  


## Logging: 
On linux system use `tail ./server.log`  
On Windows system use `get-content .\server.log -Wait`  
