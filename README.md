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

1. Edite o texto em `src/pages/*.html`, ou os dados fixos (WhatsApp, preço "a partir de", domínio) no bloco `CONFIG` do `build.py`.
2. Gere de novo: `python build.py` (gera `dist/`) e `python build.py --previa` (gera `previa/`).
3. Imagens de compartilhamento e favicons: `python gerar_imagens.py` (precisa de Playwright). Só é necessário se a logo mudar.

Marcadores aceitos nas páginas: `{{wa:mensagem pronta}}` (link do WhatsApp com a mensagem preenchida), `{{icone:nome}}`, `{{cfg:chave}}`.

## Pendências antes de publicar

- [ ] (Futuro) Incluir razão social e CNPJ nas páginas Privacidade e Termos quando a empresa estiver definida
- [ ] Revisar os preços quando o piloto validar os planos (hoje: Grátis + "a partir de R$ 149")

## Regras de comunicação (não negociáveis)

- Mote: agentes autônomos que trabalham pela operação. Sem IoT, sem sensores.
- Nunca citar tecnologias ou fornecedores por trás da solução.
- Não citar Moinho Digital nem clientes de projetos sob medida sem autorização.
- PecSmart só no rodapé e no "Quem somos".
- Anti-promessa: o site só afirma o que o agente já faz.

Na prévia aberta por duplo clique, a fonte Manrope pode não carregar (restrição do navegador para arquivos locais). No site publicado ela carrega normalmente.
