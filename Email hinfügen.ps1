
$user= Read-Host "Enter username (Example : w.saad)"
$userexist= Get-ADUser -Identity $user 
$emailadress=Read-Host "Enter Email (Example : w.saad@domain.com)"
"Databases:
Mailbox_SR 
Mailbox_BR
Mailbox_TW
Mailbox_HG"
$database= Read-Host "Enter Database " 
Enable-Mailbox -Identity $user -Database $database
#Set-Mailbox -Identity "t.test5" -EmailAddresses @{add="smtp:t.test5@hessgroup.com"}
Set-Mailbox -Identity $user -PrimarySmtpAddress $emailadress -EmailAddressPolicyEnabled $false
$checkemail=Get-Mailbox -Identity $user
if ($checkemail) {
    Write-Output "the Email has been created. Email: "$checkemail.PrimarySmtpAddress
}else {
    Write-Output "Error"
}

C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe