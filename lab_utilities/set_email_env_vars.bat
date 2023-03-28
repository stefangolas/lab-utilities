
@echo off

  set /p lab_utilities_email=Enter your email address: 
  set /p lab_utilities_password=Enter your email password: 

set /p consent=This function will set environment variables for your email address and password. Do you want to proceed? (y/n)
if /i "%consent%"=="y" (
  setx lab_utilities_email %lab_utilities_email%
  setx lab_utilities_email_password %lab_utilities_password%
  echo Environment variables set successfully.
) else (
  echo Operation cancelled.
)
