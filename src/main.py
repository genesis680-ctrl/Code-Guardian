import os
import re
import sys

# Padrões que indicam perigo (Isso é a "inteligência" do seu software)
# No futuro, empresas pagam para ter regras personalizadas aqui.
REGRAS = [
    (r"AKIA[0-9A-Z]{16}", "CRÍTICO: Chave AWS Exposta"),
    (r"-----BEGIN PRIVATE KEY-----", "CRÍTICO: Chave Privada RSA"),
    (r"password\s*=\s*['\"].+['\"]", "ALTO: Senha em texto plano"),
    (r"api_key\s*=\s*['\"].+['\"]", "MÉDIO: API Key detectada"),
]

def scan_file(filepath):
    """Lê um arquivo e procura por vulnerabilidades."""
    issues = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for i, line in enumerate(f, 1):
                for pattern, severity in REGRAS:
                    if re.search(pattern, line):
                        issues.append(f"   [Linha {i}] {severity}")
    except Exception as e:
        print(f"[!] Erro ao ler {filepath}: {e}")
    return issues

def main():
    print("🛡️  CODE-GUARDIAN v1.0 - Iniciando Auditoria...\n")
    
    target_dir = "." # Varre a pasta atual
    total_issues = 0
    
    # Caminha por todas as pastas (recursivo)
    for root, _, files in os.walk(target_dir):
        if ".git" in root: continue # Ignora a pasta oculta do Git
        
        for file in files:
            if file.endswith(".py") and file != "main.py":
                full_path = os.path.join(root, file)
                issues = scan_file(full_path)
                
                if issues:
                    print(f"❌ PROBLEMA EM: {full_path}")
                    for issue in issues:
                        print(issue)
                    total_issues += len(issues)
                    print("-" * 30)

    print("\n" + "="*40)
    if total_issues > 0:
        print(f"🔴 FALHA: {total_issues} vulnerabilidades encontradas.")
        sys.exit(1) # Retorna ERRO para o sistema (bloqueia deploy)
    else:
        print("🟢 SUCESSO: Código seguro.")
        sys.exit(0)

if __name__ == "__main__":
    main()

