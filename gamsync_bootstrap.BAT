:: Set up environment variables.
set gamdirectory=C:\gamadv-xtd3
set directory=C:\gamsync\automate\servicemanagement_*\

:: Set up folder and file export data.
set groupquery=%directory%groupquery.csv
set accountquery=%directory%accountquery.csv
set accountcleanedquery=%directory%accountcleanedquery.csv
set accountfieldquery=%directory%accountfieldquery.csv

:: Functions for handling data.
set function_accountclean=%directory%function_accountclean.py
set function_accountupdate=%directory%function_accountupdate.py
set function_accountconsolidation=%directory%function_accountconsolidation.py
set function_log=%directory%function_log.ps1
set function_sentinel=%directory%function_sentinel.ps1

:: Run logging function.
cd "%directory%"
powershell.exe -ExecutionPolicy Bypass -File %function_log%

:: Change directory to where GAM is located.
cd %gamdirectory%

:: Execute the Python script to compair changes in the share to the *al database and create accountfieldupdate.csv
python %function_accountupdate%

:: Execute the Python script to reformat accountfieldupdate.csv into CSVs with matching headers.
python %function_accountconsolidation%

:: Run GAM command to upload attribute changes from the shared database.
gam csv %directory%primaryEmail_customSchemas_*.csv gam update user "~primaryEmail" * "~customSchemas.*"
gam csv %directory%primaryEmail_customSchemas_*.csv gam update user "~primaryEmail" * "~primaryEmail,customSchemas.*"

:: Run GAM command to print groups matching the query "email:**" and save the output to a CSV file.
gam print groups query "email:**" > %groupquery%

:: Run GAM command to print group members for each group listed in the previous CSV and save the output to a CSV file.
gam csv %groupquery% gam print groupmembers group ~email > %accountquery%

:: Execute the Python script to reformat accountquery.csv onto accountqueryupdate.csv so it can be read by next process.
python %function_accountclean%

:: Run GAM command to print custom user data for the accounts listed in the cleaned CSV and put the results in a CSV file.
gam csv %accountcleanedquery% gam user ~email print custom all > %accountfieldquery%

:: Creates a copy of the accountfieldquery into a share for administrative changes to be made and then compared & uploaded later.
copy %accountfieldquery% %directory%*\accountdatabase.csv
del /Q "%directory%primaryemail*.csv"

exit