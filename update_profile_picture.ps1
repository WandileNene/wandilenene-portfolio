# Portfolio Profile Picture Update Script
# Quick script to update your profile picture

param(
    [Parameter(Mandatory=$true)]
    [string]$ImageUrl,
    
    [Parameter(Mandatory=$false)]
    [string]$ApiUrl = "http://localhost:8000",
    
    [Parameter(Mandatory=$false)]
    [int]$ProfileId = 1
)

Write-Host "🖼️  Portfolio Profile Picture Updater" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Test if backend is running
Write-Host "🔍 Checking if backend is running..." -ForegroundColor Yellow
try {
    $testResponse = Invoke-RestMethod -Uri "$ApiUrl/api/v1/profile/$ProfileId" -Method GET -ErrorAction Stop
    Write-Host "✅ Backend is running!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Current profile:" -ForegroundColor Cyan
    Write-Host "  Name: $($testResponse.full_name)" -ForegroundColor White
    Write-Host "  Title: $($testResponse.title)" -ForegroundColor White
    Write-Host "  Current Image: $($testResponse.profile_image)" -ForegroundColor White
    Write-Host ""
}
catch {
    Write-Host "❌ Error: Backend is not running!" -ForegroundColor Red
    Write-Host "Please start the backend first:" -ForegroundColor Yellow
    Write-Host "  cd backend" -ForegroundColor White
    Write-Host "  python run.py" -ForegroundColor White
    exit 1
}

# Update profile picture
Write-Host "📸 Updating profile picture..." -ForegroundColor Yellow
Write-Host "New image URL: $ImageUrl" -ForegroundColor White
Write-Host ""

try {
    $body = @{
        profile_image = $ImageUrl
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "$ApiUrl/api/v1/profile/$ProfileId" `
        -Method PATCH `
        -ContentType "application/json" `
        -Body $body `
        -ErrorAction Stop

    Write-Host "✅ Profile picture updated successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Updated profile:" -ForegroundColor Cyan
    Write-Host "  Name: $($response.full_name)" -ForegroundColor White
    Write-Host "  Title: $($response.title)" -ForegroundColor White
    Write-Host "  Image: $($response.profile_image)" -ForegroundColor White
    Write-Host ""
    Write-Host "🎉 Done! Refresh your browser to see the changes." -ForegroundColor Green
    Write-Host "   Frontend: http://localhost:5173" -ForegroundColor Cyan
}
catch {
    Write-Host "❌ Error updating profile picture!" -ForegroundColor Red
    Write-Host "Error details: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "💡 Tip: Clear browser cache if you don't see changes (Ctrl+Shift+R)" -ForegroundColor Yellow
