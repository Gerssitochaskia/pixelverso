$DST  = "C:\Users\elbol\PROYECTOS\pixelverso\images"
$BASE = "C:\Users\elbol\PROYECTOS\pixelverso"

Write-Host "=== PIXELVERSO SYNC + DEPLOY ===" -ForegroundColor Cyan

# 1. REGENERAR productos.json
Write-Host "2. Regenerando productos.json..." -ForegroundColor Yellow
Add-Type -AssemblyName System.Drawing

$catNames = @{}
$catNames["anime"]         = "Anime"
$catNames["autos"]         = "Autos"
$catNames["collage"]       = "Collage"
$catNames["cristiana"]     = "Cristiana"
$catNames["dc"]            = "DC Comics"
$catNames["deportes"]      = "Deportes"
$catNames["dragonball"]    = "Dragon Ball Z"
$catNames["enamorados"]    = "Enamorados"
$catNames["familia"]       = "Cuadros familiares"
$catNames["johnwick"]      = "John Wick"
$catNames["mafia"]         = "Mafia"
$catNames["marvel"]        = "Marvel"
$catNames["musica"]        = "Musica"
$catNames["nintendo"]      = "Nintendo"
$catNames["peliculas"]     = "Peliculas"
$catNames["personalizado"] = "Espacio personalizado"
$catNames["pokemon"]       = "Pokemon"
$catNames["strangerthings"]= "Stranger Things"
$catNames["thelastofus"]   = "The Last of Us"
$catNames["videojuegos"]   = "Videojuegos"

$productos = [System.Collections.Generic.List[object]]::new()
$cats = Get-ChildItem $DST -Directory | Sort-Object Name

foreach ($cat in $cats) {
    $catDir = "$DST\$($cat.Name)"
    $allFiles = Get-ChildItem $catDir -Filter "*.jpg" | Sort-Object Name
    $nums = [System.Collections.Generic.List[int]]::new()
    foreach ($f in $allFiles) {
        if ($f.Name -match "^$($cat.Name)-(\d+)-mockup-80x60\.jpg$") {
            $nums.Add([int]$Matches[1])
        }
    }

    foreach ($n in $nums) {
        $nn = $n.ToString("00")
        $imgPath = "$catDir\$($cat.Name)-$nn-mockup-80x60.jpg"
        $orient = "vertical"
        try {
            $img = [System.Drawing.Image]::FromFile($imgPath)
            if ($img.Width -gt $img.Height) { $orient = "horizontal" }
            $img.Dispose()
        } catch {}

        $catDisplay = if ($catNames.ContainsKey($cat.Name)) { $catNames[$cat.Name] } else { $cat.Name }
        $obj = [ordered]@{
            id          = "$($cat.Name)-$nn"
            nombre      = "$catDisplay #$([int]$nn)"
            mockup40    = "images/$($cat.Name)/$($cat.Name)-$nn-mockup-40x30.jpg"
            mockup80    = "images/$($cat.Name)/$($cat.Name)-$nn-mockup-80x60.jpg"
            art         = "images/$($cat.Name)/$($cat.Name)-$nn-art.jpg"
            categoria   = $catDisplay
            orientacion = $orient
        }
        $productos.Add($obj)
    }
}

$jsonObj = [ordered]@{ productos = $productos }
$jsonStr = $jsonObj | ConvertTo-Json -Depth 5
[System.IO.File]::WriteAllText("$BASE\data\productos.json", $jsonStr, [System.Text.UTF8Encoding]::new($false))
Write-Host "   OK: $($productos.Count) productos en $($cats.Count) categorias" -ForegroundColor Green

# 3. GIT COMMIT + PUSH
Write-Host "3. Subiendo a GitHub..." -ForegroundColor Yellow
Set-Location $BASE

# Restaurar archivos eliminados accidentalmente antes de commitear
$deleted = git ls-files --deleted 2>&1
if ($deleted) {
    Write-Host "   Restaurando archivos eliminados..." -ForegroundColor Yellow
    git checkout -- $deleted.Split("`n") 2>&1 | Out-Null
}

# Solo agregar archivos modificados/nuevos, nunca eliminar
git add data/productos.json index.html 2>&1 | Out-Null
git add images/ 2>&1 | Out-Null
git restore --staged $(git diff --name-only --diff-filter=D --cached 2>&1) 2>&1 | Out-Null

$gitStatus = git status --short 2>&1
if ($gitStatus) {
    $fecha = Get-Date -Format "yyyy-MM-dd HH:mm"
    git commit -m "sync: actualizacion $fecha" 2>&1 | Out-Null
    git push origin main 2>&1 | Out-Null
    Write-Host "   OK: subido a GitHub" -ForegroundColor Green
} else {
    Write-Host "   Sin cambios nuevos" -ForegroundColor Gray
}

# 4. LIMPIAR VERSIONES VIEJAS DE FIREBASE (mantener solo las 2 ultimas)
Write-Host "4. Limpiando versiones viejas de Firebase..." -ForegroundColor Yellow
try {
    $cfg = Get-Content "C:\Users\elbol\.config\configstore\firebase-tools.json" -Raw | ConvertFrom-Json
    $rt = $cfg.tokens.refresh_token
    $b = "grant_type=refresh_token&refresh_token=$([Uri]::EscapeDataString($rt))&client_id=563584335869-fgrhgmd47bqnekij5i8b5pr03ho849e6.apps.googleusercontent.com&client_secret=j9iVZfS8kkCEFUPaAeJV0sAi"
    $tk = (Invoke-RestMethod -Method Post -Uri "https://oauth2.googleapis.com/token" -Body $b -ContentType "application/x-www-form-urlencoded").access_token
    $vs = (Invoke-RestMethod -Uri "https://firebasehosting.googleapis.com/v1beta1/projects/-/sites/pixelverso-studio/versions?pageSize=25" -Headers @{ Authorization = "Bearer $tk" }).versions
    $old = $vs | Sort-Object createTime | Select-Object -SkipLast 2
    foreach ($v in $old) {
        Invoke-RestMethod -Method Delete -Uri "https://firebasehosting.googleapis.com/v1beta1/$($v.name)" -Headers @{ Authorization = "Bearer $tk" } | Out-Null
    }
    if ($old.Count -gt 0) { Write-Host "   Eliminadas $($old.Count) versiones viejas" -ForegroundColor Gray }
    else { Write-Host "   Sin versiones viejas" -ForegroundColor Gray }
} catch { Write-Host "   (limpieza omitida)" -ForegroundColor Gray }

# 5. FIREBASE DEPLOY
Write-Host "5. Desplegando Firebase..." -ForegroundColor Yellow
firebase login:use respetadoresdocentes@gmail.com 2>&1 | Out-Null
firebase use pixelverso-studio 2>&1 | Out-Null
$deployResult = firebase deploy --only hosting 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "   OK: https://pixelverso-studio.web.app" -ForegroundColor Green
} else {
    Write-Host "   ERROR en deploy:" -ForegroundColor Red
    $deployResult | Select-String "Error" | ForEach-Object { Write-Host "   $_" -ForegroundColor Red }
}

Write-Host "=== LISTO ===" -ForegroundColor Cyan
