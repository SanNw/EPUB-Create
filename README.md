# EPUB-Create

Create, refine, and validate EPUBs with editorial fidelity.

[![Version 0.1.0](assets/badges/version.svg)](plugin.json)
[![MIT license](assets/badges/license.svg)](LICENSE)
[![Agent Skills format](assets/badges/format.svg)](#english)
[![Skill and plugin packages](assets/badges/distribution.svg)](#english)
[![KDP guidance, not certification](assets/badges/kdp.svg)](skills/epub-create/references/kdp.md)

[English](#english) · [Português](#portugues) · [Español](#espanol)

---

<a id="english"></a>
## English

**EPUB-Create is a skill and plugin for AI agents**, not a standalone converter. It guides the creation and refinement of reflowable ebooks, preserving approved text and separating editorial decisions from technical validation.

### Features

- Approved manuscript and visual reference kept separate; originals preserved.
- Project-specific profiles, semantic headings, navigation, notes, fonts, and images.
- Researched classification of names, work titles, and foreign terms; read-only italic consistency audit.
- Amazon KDP preparation profile with official sources and a consultation date.
- One shared Agent Skills folder, a portable plugin manifest, and Claude Code plugin metadata. No hooks, bundled MCP server, authentication service, or telemetry.

Books, commercial fonts, publisher logos, and ornaments are **not included**. User-supplied resources retain their own licensing requirements. This project is not affiliated with Amazon, OpenAI, Anthropic, Cursor, or any publisher.

### Install and use

**Codex — skill:** ask Codex:

```text
$skill-installer install https://github.com/SanNw/EPUB-Create/tree/main/skills/epub-create
```

Then invoke `$epub-create`. Start a new session if it is not detected. For a local plugin, clone this repository and open it as a project in a compatible host. Its `.agents/plugins/marketplace.json` points to the plugin root. In Codex CLI, open `/plugins` and look for `epub-create` under `epub-create-local`.

**Claude Code — plugin:**

```text
/plugin marketplace add SanNw/EPUB-Create
/plugin install epub-create@epub-create
```

After installation, use `/epub-create:epub-create`. Alternatively, copy the complete skill folder to `.claude/skills/epub-create` in your project and invoke `/epub-create`.

**Cursor — skill:** copy the complete `skills/epub-create` folder to `.cursor/skills/epub-create` in your project. Use `/epub-create` or automatic discovery where supported. This is a skill installation, not a native Cursor plugin.

Do not copy only `SKILL.md`: references and helpers are part of the package. Do not overwrite a customized installation without checking its changes. Other Agent Skills hosts can use the same folder in their documented location. `agents/openai.yaml` is optional Codex metadata.

Example request:

```text
Use EPUB-Create to convert my approved ODT into a reflowable EPUB.
The PDF is only a visual reference. Destination: Amazon KDP.
Do not rewrite the text or import PDF content without permission.
```

### Requirements and checks

The agent needs local files, command execution, and web research; the plugin does not grant those capabilities. Python 3.10+ runs the package checker and editorial auditor using the standard library. Only the optional Roman numeral helper requires `lxml`. Use EPUBCheck with Java for conformance, a reader for visual checks, and Kindle Previewer for Kindle conversion. Use an appropriate local converter when needed; do not install dependencies or upload manuscripts without authorization.

Run from the repository root:

```bash
python3 skills/epub-create/scripts/epub_package.py check book.epub
python3 skills/epub-create/scripts/editorial_audit.py book.epub registry.json
python3 skills/epub-create/scripts/editorial_audit.py --self-test
python3 tests/check_package.py
```

See the [editorial guide, in Portuguese](skills/epub-create/references/editorial-standard.md) for the registry format. The auditor checks markup and inline styles, not computed CSS, source reliability, or unclassified terms. EPUBCheck does not assess editorial meaning.

### KDP and validation status

Read the [KDP profile, in Portuguese](skills/epub-create/references/kdp.md) and recheck the [official guidelines](https://kdp.amazon.com/pt_BR/help/topic/GU72M65VRFPH43L6) before delivery. EPUB validity does not guarantee Kindle conversion quality or publishing approval. EPUB.js is not a substitute for Kindle Previewer.

Verified: scripts, EPUB packaging round-trip, unsafe ZIP rejection, portable manifest schema, native Claude manifest validation, and installing the skill from GitHub. **Full conversions in separate Codex/Claude sessions and Cursor UI installation have not been completed.** Local plugin discovery depends on host version. The plugin is not approved or listed in an official directory.

### Contributions and license

Open an issue with a minimal example you own. Do not upload copyrighted books, private data, or commercial fonts. Preserve text and originals; distinguish official requirements from editorial preferences.

[MIT](LICENSE), version 0.1.0. The license covers this repository, not third-party materials or linked documentation. The plugin does not transmit data on its own; agent tools have their own permissions and policies.

Documentation: [Codex skills](https://learn.chatgpt.com/docs/build-skills) · [Portable plugins](https://developers.openai.com/plugins/build/plugins) · [Claude marketplaces](https://code.claude.com/docs/en/plugin-marketplaces) · [Cursor skills](https://cursor.com/docs/context/skills).

---

<a id="portugues"></a>
## Português

**EPUB-Create é uma skill e um plugin para agentes de IA**, não um conversor autônomo. Orienta a criação e o refinamento de ebooks refluíveis, preservando o texto aprovado e separando decisões editoriais de validação técnica.

### Recursos

- Separação entre manuscrito aprovado e referência visual, preservando os originais.
- Perfis por projeto, títulos semânticos, navegação, notas, fontes e imagens.
- Classificação pesquisada de nomes, títulos de obras e estrangeirismos; auditoria de consistência dos itálicos somente de leitura.
- Perfil de preparação para Amazon KDP com fontes oficiais e data de consulta.
- Uma pasta Agent Skills compartilhada, manifesto de plugin portátil e metadados de plugin para Claude Code. Sem hooks, MCP próprio, serviço de autenticação ou telemetria.

Livros, fontes comerciais, logos e ornamentos de editoras **não estão incluídos**. Os recursos fornecidos pelo usuário continuam sujeitos às próprias licenças. O projeto não é afiliado à Amazon, OpenAI, Anthropic, Cursor ou a editoras.

### Instalação e uso

**Codex — skill:** solicite no Codex:

```text
$skill-installer instale https://github.com/SanNw/EPUB-Create/tree/main/skills/epub-create
```

Depois invoque `$epub-create`. Abra nova sessão se ela não for detectada. Para o plugin local, clone o repositório e abra-o como projeto em um host compatível. O arquivo `.agents/plugins/marketplace.json` aponta à raiz do plugin. No Codex CLI, abra `/plugins` e procure `epub-create` em `epub-create-local`.

**Claude Code — plugin:**

```text
/plugin marketplace add SanNw/EPUB-Create
/plugin install epub-create@epub-create
```

Após instalar, use `/epub-create:epub-create`. Alternativamente, copie a skill completa para `.claude/skills/epub-create` no projeto e invoque `/epub-create`.

**Cursor — skill:** copie a pasta completa `skills/epub-create` para `.cursor/skills/epub-create` no projeto. Use `/epub-create` ou descoberta automática quando disponível. É uma instalação de skill, não um plugin nativo do Cursor.

Não copie apenas o `SKILL.md`: referências e helpers fazem parte do pacote. Não sobrescreva uma instalação personalizada sem conferir suas alterações. Outros hosts Agent Skills podem usar a mesma pasta no local documentado por eles. `agents/openai.yaml` é metadado opcional do Codex.

Exemplo de pedido:

```text
Use EPUB-Create para converter meu ODT aprovado em EPUB refluível.
O PDF é somente referência visual. Destino: Amazon KDP.
Não reescreva o texto nem importe conteúdo do PDF sem autorização.
```

### Requisitos e verificações

O agente precisa de arquivos locais, execução de comandos e pesquisa web; o plugin não concede essas capacidades. Python 3.10+ executa o verificador de pacote e o auditor editorial com a biblioteca padrão. Apenas o helper opcional de romanos requer `lxml`. Use EPUBCheck com Java para conformidade, um leitor para conferência visual e Kindle Previewer para conversão Kindle. Utilize conversor local adequado quando necessário; não instale dependências nem envie manuscritos sem autorização.

Execute a partir da raiz do repositório:

```bash
python3 skills/epub-create/scripts/epub_package.py check livro.epub
python3 skills/epub-create/scripts/editorial_audit.py livro.epub registro.json
python3 skills/epub-create/scripts/editorial_audit.py --self-test
python3 tests/check_package.py
```

Consulte o [guia editorial](skills/epub-create/references/editorial-standard.md) para o formato do registro. O auditor verifica marcação e estilos inline, não a cascata CSS, a confiabilidade das fontes ou termos não classificados. EPUBCheck não avalia significado editorial.

### KDP e estado da validação

Leia o [perfil KDP](skills/epub-create/references/kdp.md) e confira novamente as [diretrizes oficiais](https://kdp.amazon.com/pt_BR/help/topic/GU72M65VRFPH43L6) antes da entrega. Validade EPUB não garante qualidade da conversão Kindle nem aprovação para publicação. EPUB.js não substitui Kindle Previewer.

Verificado: scripts, ciclo de extração/empacotamento EPUB, rejeição de ZIP inseguro, esquema do manifesto portátil, validação nativa dos manifests Claude e instalação da skill a partir do GitHub. **Não foram concluídas conversões completas em sessões separadas de Codex/Claude nem instalação pela interface do Cursor.** A descoberta do plugin local depende da versão do host. O plugin não está aprovado nem listado em diretório oficial.

### Contribuições e licença

Abra uma issue com um exemplo mínimo de sua autoria. Não envie livros protegidos, dados privados ou fontes comerciais. Preserve texto e originais; diferencie requisitos oficiais de preferências editoriais.

[MIT](LICENSE), versão 0.1.0. A licença cobre este repositório, não materiais de terceiros nem documentação vinculada. O plugin não transmite dados por conta própria; ferramentas do agente têm suas próprias permissões e políticas.

Documentação: [Skills do Codex](https://learn.chatgpt.com/docs/build-skills) · [Plugins portáteis](https://developers.openai.com/plugins/build/plugins) · [Marketplaces Claude](https://code.claude.com/docs/en/plugin-marketplaces) · [Skills do Cursor](https://cursor.com/docs/context/skills).

---

<a id="espanol"></a>
## Español

**EPUB-Create es una skill y un plugin para agentes de IA**, no un conversor autónomo. Orienta la creación y el refinamiento de ebooks reajustables, preservando el texto aprobado y separando las decisiones editoriales de la validación técnica.

### Funciones

- Separación entre manuscrito aprobado y referencia visual, conservando los originales.
- Perfiles por proyecto, encabezados semánticos, navegación, notas, fuentes e imágenes.
- Clasificación investigada de nombres, títulos de obras y extranjerismos; auditoría de coherencia de cursivas de solo lectura.
- Perfil de preparación para Amazon KDP con fuentes oficiales y fecha de consulta.
- Una carpeta Agent Skills compartida, manifiesto de plugin portátil y metadatos de plugin para Claude Code. Sin hooks, servidor MCP propio, servicio de autenticación ni telemetría.

Los libros, fuentes comerciales, logotipos y ornamentos editoriales **no están incluidos**. Los recursos aportados por el usuario mantienen sus propias licencias. El proyecto no está afiliado a Amazon, OpenAI, Anthropic, Cursor ni a editoriales.

### Instalación y uso

**Codex — skill:** solicita en Codex:

```text
$skill-installer instala https://github.com/SanNw/EPUB-Create/tree/main/skills/epub-create
```

Después invoca `$epub-create`. Abre una nueva sesión si no se detecta. Para el plugin local, clona el repositorio y ábrelo como proyecto en un entorno compatible. `.agents/plugins/marketplace.json` apunta a la raíz del plugin. En Codex CLI, abre `/plugins` y busca `epub-create` en `epub-create-local`.

**Claude Code — plugin:**

```text
/plugin marketplace add SanNw/EPUB-Create
/plugin install epub-create@epub-create
```

Después de instalar, usa `/epub-create:epub-create`. Como alternativa, copia la skill completa a `.claude/skills/epub-create` en el proyecto e invoca `/epub-create`.

**Cursor — skill:** copia toda la carpeta `skills/epub-create` a `.cursor/skills/epub-create` en el proyecto. Usa `/epub-create` o el descubrimiento automático cuando esté disponible. Es una instalación de skill, no un plugin nativo de Cursor.

No copies solo `SKILL.md`: las referencias y los helpers forman parte del paquete. No sobrescribas una instalación personalizada sin revisar sus cambios. Otros entornos Agent Skills pueden utilizar la misma carpeta en la ubicación que documenten. `agents/openai.yaml` contiene metadatos opcionales de Codex.

Ejemplo de solicitud:

```text
Usa EPUB-Create para convertir mi ODT aprobado en un EPUB reajustable.
El PDF es solo una referencia visual. Destino: Amazon KDP.
No reescribas el texto ni importes contenido del PDF sin autorización.
```

### Requisitos y comprobaciones

El agente necesita archivos locales, ejecución de comandos e investigación web; el plugin no concede estas capacidades. Python 3.10+ ejecuta el verificador de paquetes y el auditor editorial con la biblioteca estándar. Solo el helper opcional de números romanos requiere `lxml`. Usa EPUBCheck con Java para conformidad, un lector para revisión visual y Kindle Previewer para conversión Kindle. Utiliza un conversor local apropiado cuando haga falta; no instales dependencias ni envíes manuscritos sin autorización.

Ejecuta desde la raíz del repositorio:

```bash
python3 skills/epub-create/scripts/epub_package.py check libro.epub
python3 skills/epub-create/scripts/editorial_audit.py libro.epub registro.json
python3 skills/epub-create/scripts/editorial_audit.py --self-test
python3 tests/check_package.py
```

Consulta la [guía editorial, en portugués](skills/epub-create/references/editorial-standard.md) para el formato del registro. El auditor comprueba marcado y estilos inline, no la cascada CSS, la fiabilidad de las fuentes ni términos sin clasificar. EPUBCheck no evalúa el significado editorial.

### KDP y estado de validación

Lee el [perfil KDP, en portugués](skills/epub-create/references/kdp.md) y vuelve a comprobar las [directrices oficiales](https://kdp.amazon.com/pt_BR/help/topic/GU72M65VRFPH43L6) antes de entregar. La validez EPUB no garantiza calidad de conversión Kindle ni aprobación para publicar. EPUB.js no sustituye a Kindle Previewer.

Verificado: scripts, ciclo de extracción/empaquetado EPUB, rechazo de ZIP inseguro, esquema del manifiesto portátil, validación nativa de manifests Claude e instalación de la skill desde GitHub. **No se han completado conversiones integrales en sesiones independientes de Codex/Claude ni instalación desde la interfaz de Cursor.** El descubrimiento del plugin local depende de la versión del entorno. El plugin no está aprobado ni incluido en un directorio oficial.

### Contribuciones y licencia

Abre una issue con un ejemplo mínimo de tu autoría. No envíes libros protegidos, datos privados ni fuentes comerciales. Preserva texto y originales; distingue requisitos oficiales de preferencias editoriales.

[MIT](LICENSE), versión 0.1.0. La licencia cubre este repositorio, no materiales de terceros ni documentación enlazada. El plugin no transmite datos por sí mismo; las herramientas del agente tienen sus propios permisos y políticas.

Documentación: [Skills de Codex](https://learn.chatgpt.com/docs/build-skills) · [Plugins portátiles](https://developers.openai.com/plugins/build/plugins) · [Marketplaces Claude](https://code.claude.com/docs/en/plugin-marketplaces) · [Skills de Cursor](https://cursor.com/docs/context/skills).
