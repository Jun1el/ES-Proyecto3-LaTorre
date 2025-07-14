#!/usr/bin/env bash
# Script de CI/CD 
# Verifica si las herramientas necesarias estan instaladas
check_tools() {
    for tool in black flake8 shellcheck pytest pytest-mock pytest-cov pytest-asyncio ; do
        if ! command -v $tool &> /dev/null; then
            echo "Error: $tool no está instalado."
            exit 1
        fi
    done
}
# Ejecutamos black para formatear el codigo
run_black() {
    echo "Ejecutando black..."
    black src/
    if [ $? -ne 0 ]; then
        echo "Error black encontro problemas de formato."
        exit 1
    fi
}
# Ejecuta flake8 para verificar el estilo del codigo
run_flake8() {
    echo "Ejecutando flake8..."
    flake8 src/
    if [ $? -ne 0 ]; then
        echo "Error: flake8 encontro problemas de estilo."
        exit 1
    fi
}
# Ejecuta shellcheck para verificar el script de CI/CD
run_shellcheck() {
    echo "Ejecutando shellcheck..."
    shellcheck scripts/ci.sh
    if [ $? -ne 0 ]; then
        echo "Error: shellcheck encontro problemas en el script de CI/CD."
        exit 1
    fi
}