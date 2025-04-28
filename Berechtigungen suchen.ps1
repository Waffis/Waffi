# Zeigt alle Postfächer, auf die ein Benutzer Zugriffsrechte hat
"Zeigt alle Postfächer, auf die ein Benutzer Zugriffsrechte hat"
Connect-ExchangeOnline

$email= Read-Host "gib die Email ein"
Get-Mailbox -ResultSize Unlimited | ForEach-Object{
    $permission= Get-MailboxPermission $_.DistinguishedName | Where-Object{$_.User -eq $email -and $_.AccessRights -ne "None"}
    foreach ($perm in $permission){

        [PSCustomObject]@{
            MailboxName         = $_.Name
            MailboxEmail        = $_.PrimarySmtpAddress
            UserHasPermission   = $perm.User
            AccessRights        = $perm.AccessRights -join ", "
            IsInherited         = $perm.IsInherited
        }

    }

}
