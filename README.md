# EPUB-Create

Skill e plugin para agentes criarem, refinarem e validarem EPUBs com fidelidade editorial, pesquisa de itálicos e preparação técnica para Amazon KDP.

Versão inicial: **0.1.0**. Licença MIT. Não afiliado à Amazon, OpenAI ou a editoras. É um fluxo assistido por agente, não um aplicativo autônomo de conversão nem garantia de publicação.

## O que inclui

- Separação entre manuscrito aprovado e referência visual, perfis por projeto e preservação dos originais.
- Hierarquia, sumário, notas, fontes, imagens e conferência entre leitores.
- Pesquisa contextual de nomes próprios, títulos e estrangeirismos; auditor lexical somente de leitura.
- Perfil KDP com fontes oficiais e data de consulta. Requisitos de publicação devem ser revalidados.
- Plugin portátil com uma skill, sem hooks, MCP próprio, autenticação nem coleta de telemetria.

Não inclui livros, fontes comerciais, logos ou ornamentos de editoras. Os recursos fornecidos pelo usuário continuam sujeitos às respectivas licenças.

## Instalar a skill no Codex

No Codex, solicite:

```text
$skill-installer instale https://github.com/SanNw/EPUB-Create/tree/main/skills/epub-create
```

Depois invoque `$epub-create`. Se não aparecer, abra nova sessão. Alternativamente, copie a pasta `skills/epub-create` para um diretório de skills reconhecido pelo seu agente. [Documentação oficial de skills](https://learn.chatgpt.com/docs/build-skills).

Exemplo:

```text
Use $epub-create para converter meu ODT aprovado em EPUB refluível.
O PDF é somente referência visual. Destino: Amazon KDP.
Não altere o texto nem importe conteúdo do PDF sem autorização.
```

## Usar como plugin local

O repositório é também a raiz do plugin: `plugin.json` + `skills/`. Contém um marketplace de projeto em `.agents/plugins/marketplace.json`, apontando à própria raiz, sem duplicar a skill.

1. Clone o repositório e abra esse projeto em um host compatível.
2. Use o navegador de plugins (no Codex CLI: `/plugins`) e confira a entrada `epub-create` no marketplace `epub-create-local`.
3. Instale e inicie nova sessão para usar a skill incluída. Se o host exigir reinício para descobrir o marketplace, reinicie-o.

O pacote foi preparado para instalação local, mas a descoberta/instalação pela interface pode variar por versão do host. Não está listado nem aprovado no diretório universal. [Empacotamento oficial de plugins](https://developers.openai.com/plugins/build/plugins).

## Claude Code e Cursor

A mesma pasta `skills/epub-create` segue Agent Skills, sem ferramentas exclusivas de um agente nas instruções. `agents/openai.yaml` é metadado opcional do Codex; outros hosts podem ignorá-lo.

**Claude Code — plugin:** o repositório inclui `.claude-plugin/plugin.json` e marketplace próprio. No Claude Code:

```text
/plugin marketplace add SanNw/EPUB-Create
/plugin install epub-create@epub-create
```

Após instalar, confira o comando com namespace `/epub-create:epub-create`. Como alternativa, copie a skill completa para `.claude/skills/epub-create` no projeto e invoque `/epub-create`. [Documentação oficial de marketplaces](https://code.claude.com/docs/en/plugin-marketplaces).

**Cursor — skill:** copie a pasta completa para `.cursor/skills/epub-create` no projeto (não apenas o SKILL.md). Use `/epub-create` ou a descoberta automática conforme a versão instalada. [Documentação oficial de Agent Skills](https://cursor.com/docs/context/skills).

No Windows, use o gerenciador de arquivos; em Linux/macOS, a cópia para um projeto pode ser feita com `mkdir -p .cursor/skills` e `cp -R /caminho/EPUB-Create/skills/epub-create .cursor/skills/`. Não sobrescreva uma instalação existente sem conferir suas alterações.

**Outros agentes:** instale a pasta no local indicado pelo host para Agent Skills. A skill precisa de acesso aos arquivos, execução local e pesquisa; essas capacidades não são habilitadas pelo plugin. Não garantimos equivalência de comportamento entre modelos ou versões.

Os manifests e scripts são testados no repositório; instalações pela interface de Claude/Cursor/Codex e conversões end-to-end por esses agentes devem ser verificadas em cada ambiente. O pacote não é um plugin nativo do Cursor: nesse host, a distribuição documentada é como skill.

## Requisitos

- Agente com leitura/escrita local e pesquisa web para classificações editoriais.
- Python 3.10+ para `epub_package.py` e `editorial_audit.py` (biblioteca padrão).
- `lxml` somente para `roman_smallcaps.py`, helper opcional.
- EPUBCheck + Java para validação de conformidade. Leitor/EPUB.js para prévia visual; Kindle Previewer para teste Kindle.
- Conversor local adequado ao arquivo de origem, quando necessário. Não instale dependências nem envie manuscritos a serviços externos sem autorização.

Não é preciso copiar configurações pessoais, instalar um MCP ou fornecer chave de API própria a este pacote.

## Scripts

Execute a partir da raiz do repositório:

```bash
python3 skills/epub-create/scripts/epub_package.py check livro.epub
python3 skills/epub-create/scripts/editorial_audit.py livro.epub registro.json
python3 skills/epub-create/scripts/editorial_audit.py --self-test
python3 tests/check_package.py
```

Para o registro pesquisado e opções de auditoria, leia [Padrão editorial](skills/epub-create/references/editorial-standard.md). A auditoria não calcula CSS de classes, não identifica pessoas sozinha e não valida a veracidade de URLs. Os achados exigem avaliação contextual; EPUBCheck não verifica decisões semânticas.

## Amazon KDP

Leia o [perfil KDP](skills/epub-create/references/kdp.md), derivado de consulta às [diretrizes oficiais](https://kdp.amazon.com/pt_BR/help/topic/GU72M65VRFPH43L6). Um EPUB válido pode ainda ter problemas após a conversão Kindle. Não declare aprovação KDP sem evidência, nem confunda prévia EPUB.js com Kindle Previewer.

## Contribuições e limites

Abra uma issue com o problema e, se possível, um exemplo mínimo de sua autoria. Não envie livros protegidos, dados pessoais ou fontes comerciais. Mudanças devem manter originais intactos, preservar texto e distinguir regras oficiais de preferências editoriais.

O plugin não envia dados por conta própria; ferramentas usadas pelo agente têm suas próprias permissões e políticas. Pesquisa web não deve enviar passagens privadas inteiras. A licença MIT cobre os arquivos deste projeto, não recursos de terceiros ou as páginas oficiais citadas.
