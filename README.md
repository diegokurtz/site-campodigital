# Site institucional Campo Digital (campodigital.com.br)

Site estático, sem dependências de terceiros em tempo de execução: sem cookies, sem analytics, fontes servidas pelo próprio site.

## Pastas

| Pasta | O que é |
|---|---|
| `src/pages/` | Conteúdo de cada página (um arquivo por página, com metadados no topo) |
| `src/static/` | CSS, JS, fontes e imagens |
| `dist/` | **Site pronto para publicar** (gerado; não editar à mão) |
| `previa/` | Cópia para ver no computador com duplo clique em `previa/index.html` (só para revisão) |

## Como alterar

1. Edite o texto em `src/pages/*.html`, ou os dados fixos (WhatsApp, preços e condições dos planos, empresa, domínio) no bloco `CONFIG` do `build.py`. Preço não se digita na página: use `{{brl:preco_mensal}}` e afins.
2. Gere de novo: `python build.py` (gera `dist/`) e `python build.py --previa` (gera `previa/`).
3. Imagens de compartilhamento e favicons: `python gerar_imagens.py` (precisa de Playwright). Só é necessário se a logo mudar.

Marcadores aceitos nas páginas: `{{wa:mensagem pronta}}` (link do WhatsApp com a mensagem preenchida e a origem `[ref:...]` da página, definida por `ref:` no topo; se a mensagem já tiver `[ref:...]`, vale a dela), `{{icone:nome}}`, `{{cfg:chave}}`, `{{brl:chave}}` (R$ 1.490) e `{{brl2:chave}}` (R$ 1.490,00).

Os preços estão escritos nos Termos de Uso e Assinatura (versão em `termos_versao`). O build recusa gerar o site se o `CONFIG` divergir do que foi aprovado para essa versão: mudou preço, publique nova versão dos Termos e registre em `TERMOS_APROVADOS`.

## Pendências antes de publicar

- [x] Razão social, CNPJ e endereço (DJ KURTZ LTDA) em Privacidade, Termos e rodapé (14/10/2026)
- [x] Planos Teste 14 dias / Mensal R$ 149 / Anual R$ 1.490 / por projeto (Termos versão 2026-10)

## Regras de comunicação (não negociáveis)

- Mote: agentes autônomos que trabalham pela operação. Sem IoT, sem sensores.
- Nunca citar tecnologias ou fornecedores por trás da solução.
- Não citar Moinho Digital nem clientes de projetos sob medida sem autorização.
- PecSmart só no rodapé e no "Quem somos".
- Anti-promessa: o site só afirma o que o agente já faz.

Na prévia aberta por duplo clique, a fonte Manrope pode não carregar (restrição do navegador para arquivos locais). No site publicado ela carrega normalmente.
