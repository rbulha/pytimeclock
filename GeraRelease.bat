echo off
PATH=%PATH%;c:\python27
echo ----------------------------------------------------------------
echo Gera versão release do pyRelogio de Ponto
echo by Rogerio Bulha
echo ----------------------------------------------------------------

python -OO setup.py py2exe > LogSetup.txt

IF EXIST ..\release_pck (mkdir ..\release_pck\bin\Microsoft.VC90.CRT) ELSE (goto FALHA)
echo Copiando arquivos de distribuição VC9
copy Microsoft.VC90.CRT ..\release_pck\bin\Microsoft.VC90.CRT
goto FIM 
:FALHA
echo --------------------------------------------------------------------------
echo Copiar manualmente pasta Microsoft.VC90.CRT para diretorio de distribuição
:FIM
IF EXIST build (rmdir /S /Q build) ELSE (goto FALHA)
echo DONE
echo FIM
pause
pause
