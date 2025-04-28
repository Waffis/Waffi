$users = Get-ADUser -Filter * | Where-Object { $_.Enabled -eq $false } | Select-Object -Property UserPrincipalName

foreach ($user in $users) {
    try {

        $userExists = Get-MgUser -UserId $user.UserPrincipalName -ErrorAction SilentlyContinue
        if ($userExists) {
            $userLicenses = Get-MgUserLicenseDetail -UserId $user.UserPrincipalName
            $hasLicense = $userLicenses | Where-Object { $_.SkuPartNumber -eq "SPE_E3" }
            if ($hasLicense) {
                Write-Output "$($user.UserPrincipalName) has the SPE_E3 license."
            }
        }
    }
    catch {
        
    }
}





