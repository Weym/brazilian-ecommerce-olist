import os

outline_path = 'docs/slides_outline.md'
assert os.path.exists(outline_path), f'FAIL: {outline_path} nao existe'
content = open(outline_path, encoding='utf-8').read()
print(f'OK: slides_outline.md existe ({len(content.split())} palavras)')

# Verificar estrutura dos dois atos
for marker in ['ATO 1', 'ATO 2', 'APENDICE', 'Slide 01', 'Slide 18', 'Slide A1', 'Slide A5']:
    assert marker in content, f'FAIL: {marker} ausente no roteiro'
    print(f'OK: {marker} presente')

# Verificar frase-ancora
assert '40%' in content, 'FAIL: frase-ancora 40% ausente no roteiro'
print('OK: frase-ancora 40% no roteiro')

# Verificar referencias a figuras
assert 'pr_curve.png' in content, 'FAIL: pr_curve.png nao referenciado'
assert 'shap_beeswarm.png' in content, 'FAIL: shap_beeswarm.png nao referenciado'
print('OK: figuras principais referenciadas no roteiro')

print('PASS: slides_outline.md completo')
