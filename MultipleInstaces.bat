@echo off

set /A instances=15
set /A offset=79100000
set /A step=6250

rem python might not be in your path as py you can replace it with the direct path to your python.exe for example

FOR /L %%v IN (0 1 %instances% ) DO  (
    start /B py .\DataFetching.py %offset% %step% %%v
)

