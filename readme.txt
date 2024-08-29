Version 1.1 Author Oliver Farthing

Prerequisites
Root Folder: Ensure that the root folder is located at C:\gamsync\automate\servicerecruitment_*. 
The system does not require "gamsync" funcation.
GAM Advanced: A functional version of "GAM Advanced" must be installed in the directory C:\gamadv-xtd3.
Python: Functions on this sevice have been built in python so python will need to be installed on running system.

Components (Essential files for this service)
gamautomate_bootstrap.BAT: Initiates a new synchronization process.
function_accountclean.py: Execute the Python script to reformat accountquery.csv onto accountqueryupdate.csv so it can be read by next process.
function_accountupdate.py: Compair changes in the share to the original database and create accountfieldupdate.csv
function_accountconsolidation.py: Reformat accountfieldupdate.csv into CSVs with matching headers.
function_log.ps1: Creates backups of the uplaoded changes.
function_sentinel.py: Keeps track of changes to files and creates an audit trail.

Changes
28/08/24 - Version 1.1
Added sentinel funcation to keep track of file changes on the share folder

27/08/24 - Version 1
Service Created, See Sync Process Guide

1. Change Directory to GAM Location
Command: cd %gamdirectory%
Description
This command changes the current working directory to the one specified by the %gamdirectory% variable, where GAM (Google Apps Manager) is located.

2. Execute Python Script to Compare Database Changes
Command: python %function_accountupdate%
Description
Runs a Python script specified by the %function_accountupdate% variable. This script compares changes in the shared database and generates a file named accountfieldupdate.csv.

3. Reformat accountfieldupdate.csv
Command: python %function_accountconsolidation%
Description
Executes another Python script, defined by %function_accountconsolidation%, which reformats accountfieldupdate.csv into CSVs with matching headers for further processing.

4. Upload Attribute Changes Using GAM
gam csv %directory%primaryEmail_customSchemas_*.csv gam update user "~primaryEmail" * "~customSchemas.*"
gam csv %directory%primaryEmail_customSchemas_*.csv gam update user "~primaryEmail" * "~primaryEmail,customSchemas.*"
Description
These commands use GAM to update user attributes in Google Workspace. The first command uploads changes based on custom schemas, while the second uploads changes including both primary email and custom schemas.

5. Print Groups Matching a Query
Command: gam print groups query "email:**" > %groupquery%
Description
This GAM command retrieves a list of groups in Google Workspace that match the query "email:**" (which searches for any email), and outputs the results to a CSV file specified by %groupquery%.

6. Print Group Members
Command: gam csv %groupquery% gam print groupmembers group ~email > %accountquery%
Description
For each group listed in the previously generated CSV (%groupquery%), this command prints the members of each group and saves the data to another CSV file specified by %accountquery%.

7. Reformat accountquery.csv
Command: python %function_accountclean%
Description
Runs a Python script specified by %function_accountclean% that reformats accountquery.csv into accountqueryupdate.csv. This reformatting ensures the data can be used by subsequent processes.

8. Print Custom User Data for Accounts
Command: gam csv %accountcleanedquery% gam user ~email print custom all > %accountfieldquery%
Description
This GAM command retrieves custom user data for the accounts listed in the cleaned CSV (%accountcleanedquery%) and outputs the results to a CSV file (%accountfieldquery%).

9. Create a Copy of accountfieldquery for Administrative Changes
copy %accountfieldquery% %directory%*\accountdatabase.csv
del /Q "%directory%primaryemail*.csv"
Description
Copies the accountfieldquery CSV to a shared location (%directory%*\accountdatabase.csv) for administrative review and future comparison.
Deletes all CSV files with names starting with "primaryemail" in the specified directory to clean up temporary files.
