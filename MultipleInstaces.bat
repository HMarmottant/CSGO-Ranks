set /A instances=3
set /A offset=79000000
set /A step=10


FOR /L %%v IN (0 1 %instances% ) DO  (
    start py .\DataFetching.py %offset% %step% %%v
)

pause
