# run_test.ps1 - Suite de pruebas y cobertura para Hunter-Nexus

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Hunter-Nexus: Test Runner & Coverage " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# 1. Asegurar que pytest-cov está instalado
pip install pytest-cov -q

# 2. Ejecutar pytest con reporte de cobertura por consola y HTML
python -m pytest -v --cov=src --cov-report=term-missing --cov-report=html

# 3. Comprobar resultado de los tests
if ($LASTEXITCODE -eq 0) {
    Write-Host "`n[OK] ¡Todos los tests han pasado con exito!" -ForegroundColor Green
    Write-Host "[INFO] Reporte HTML generado en: htmlcov/index.html" -ForegroundColor Yellow
} else {
    Write-Host "`n[ERROR] Se han detectado fallos en los tests." -ForegroundColor Red
}