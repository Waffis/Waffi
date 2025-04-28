#********************Lokal anlegen*******************************
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
Set-Mailbox -Identity $user -PrimarySmtpAddress $emailadress -EmailAddressPolicyEnabled $false
$checkemail=Get-Mailbox -Identity $user
if ($checkemail) {
    $status=$checkemail.PrimarySmtpAddress
    Write-Output "the Email has been created. Email: $status"
}else {
    Write-Output "Error"
}




#********* New-MigrationBatch ****************************
Connect-ExchangeOnline
$user =  Read-Host "Ex: w.saad"
$email=  Read-Host "Ex: w.saad@hessgroup.com"
    
$csv= "EmailAddress`n$email"
New-MigrationBatch -Name "$user" `
    -CSVData ([System.Text.Encoding]::UTF8.GetBytes($csv)) `
    -SourceEndpoint "HESS" `
    -TargetDeliveryDomain "tmitservice.mail.onmicrosoft.com" `
    -AutoStart `
    -NotificationEmails "w.saad@hessgroup.com" `
    -AutoComplete

#************check***************************
if(Get-MigrationBatch -Identity $user){
    Write-Output "Wird Megrieren ... "
    Start-Sleep 300
    while ($true){
        $status = (Get-MigrationBatch $user).Status
        Write-Output "Status: $status"
        if ($status -eq 4) {
            Write-Output "done"
            break 

        } elseif ($status -eq 10) {
            Write-Output "Error" 
        }
        else {
            Write-Output "noch nicht fertig"
            Start-Sleep 300
        }
    }
}


#**************************Azure- Grouppe****************************************
# Connect-AzureAD
# $user="user"
# $userid=(Get-AzureADUser -SearchString "$user").ObjectId
# Add-AzureADGroupMember -ObjectId "1a8c6daf-3aae-4740-a093-e82643f09fd6" -RefObjectId "$userid"

#**************************check-Lizenz****************************************

Connect-MgGraph -Scopes "User.Read.All", "Directory.Read.All"

Get-MgUserLicenseDetail -UserId w.saad@hessgroup.com |ForEach-Object{
    if ($_.SkuPartNumber -contains  "SPE_E3"){
        Write-Output "hat Lizenz"
    }

}
