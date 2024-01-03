# Primeflix-movie-downloader-script.ps1

function Download-File {
    param (
        [string]$url,
        [string]$outputPath
    )

    try {
        Invoke-WebRequest -Uri $url -OutFile $outputPath -ErrorAction Stop
        Write-Host "File downloaded successfully to $outputPath"
    } catch {
        Write-Host "Failed to download the file: $_"
    }
}

function Search-Content {
    param (
        [string]$contentType
    )

    while ($true) {
        $contentName = Read-Host "Enter the $contentType name: "
        if ($contentName.Trim() -ne "") {
            break
        }
        Write-Host "Invalid input. Please enter a valid name."
    }

    $nameQuery = $contentName -split '\s+' -join '+'
    $result = Invoke-WebRequest -Uri "https://mycima.cloud/search/$nameQuery"
    $src = $result.Content
    $soup = New-Object HtmlAgilityPack.HtmlDocument
    $soup.LoadHtml($src)

    $contentInfo = $soup.DocumentNode.SelectNodes("//div[@class='Thumb--GridItem']")

    if ($contentInfo.Count -eq 0) {
        Write-Host "No matching $contentType found. Please try again."
        return $null
    }

    if ($contentInfo.Count -gt 1) {
        for ($i = 0; $i -lt $contentInfo.Count; $i++) {
            Write-Host "$($i): $($contentInfo[$i].InnerText)"
        }

        while ($true) {
            try {
                $choice = Read-Host "Choose a $contentType by entering its index"
                if ($choice -ge 0 -and $choice -lt $contentInfo.Count) {
                    return $contentInfo[$choice].SelectSingleNode("a").GetAttributeValue("href", "")
                } else {
                    Write-Host "Invalid choice. Please enter a valid index."
                }
            } catch {
                Write-Host "Invalid input. Please enter a number."
            }
        }
    } else {
        return $contentInfo[0].SelectSingleNode("a").GetAttributeValue("href", "")
    }
}

function Show-Banner {
@"
__________        .__                        ___________.__  .__        
\______   \_______|__| _____   ____          \_   _____/|  | |__|__  ___
 |     ___/\_  __ \  |/     \_/ __ \   ______ |    __)  |  | |  \  \/  /
 |    |     |  | \/  |  Y Y  \  ___/  /_____/ |     \   |  |_|  |>    < 
 |____|     |__|  |__|__|_|  /\___  >         \___  /   |____/__/__/\_ \
                           \/     \/              \/                  \/
"@
    Write-Host "Written by CHEGEBB"
}

function Main {
    Show-Banner
    Write-Host "Welcome to Primeflix"

    while ($true) {
        Write-Host "`nChoose what to download:"
        Write-Host "1. Movie"
        Write-Host "2. TV Series"
        Write-Host "3. Links to other download sites (Coming Soon)"
        Write-Host "4. Exit"

        $choice = Read-Host "Enter your choice"

        switch ($choice) {
            "1" {
                $movieLink = Search-Content -contentType "movie"
                if ($movieLink -ne $null) {
                    $outputPath = Join-Path $env:USERPROFILE "Downloads\movie_file.mp4"
                    Download-File -url $movieLink -outputPath $outputPath
                } else {
                    Write-Host "No valid download links found for the selected movie."
                }
            }
            "2" {
                $seriesLink = Search-Content -contentType "TV series"
                if ($seriesLink -ne $null) {
                    $outputPath = Join-Path $env:USERPROFILE "Downloads\series_file.mp4"
                    Download-File -url $seriesLink -outputPath $outputPath
                } else {
                    Write-Host "No valid download links found for the selected TV series."
                }
            }
            "3" {
                Write-Host "Links to other download sites functionality coming soon!"
            }
            "4" {
                Write-Host "Thank you for using Primeflix. Goodbye!"
                break
            }
            default {
                Write-Host "Invalid choice. Please enter a valid option."
            }
        }
    }
}

Main
