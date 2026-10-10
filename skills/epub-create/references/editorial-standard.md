# Padrão editorial e auditoria

## Perfis e fontes

O contrato do projeto separa fonte textual aprovada de referência visual. Um PDF antigo pode orientar diagramação, mas conteúdo ausente no manuscrito só é importado com autorização e origem registrada. Conserve texto e grafia; revisão textual é uma tarefa separada.

- **Geral:** refluível, identidade fornecida, sem adicionar logos, ornamentos ou catálogo.
- **Editora/projeto:** registre fonte, variantes, destaques, notas, citações, logo, ornamento, catálogo e ordem das preliminares. Não transforme o padrão de uma editora em regra universal. Recursos gráficos devem ser fornecidos com autorização de uso.
- **KDP:** sobrepõe requisitos de compatibilidade ao perfil visual; consulte [kdp.md](kdp.md). Se um requisito conflitar com um pedido editorial, explique o conflito e não prometa equivalência entre leitores.

## Composição

- Preserve hierarquia semântica de títulos, não use seus níveis apenas para obter tamanhos.
- Índice visível clicável, próximo do início e sem números de página por padrão. Referência numérica impressa só em perfil geral quando expressamente solicitada. Não prometa paginação adaptativa no XHTML.
- Título do índice pode ser centralizado; entradas ficam à esquerda. Corpo contínuo com recuo e sem espaços artificiais entre parágrafos, salvo padrão expresso do projeto.
- Citações em blockquote com espaço externo antes/depois e sem intervalos artificiais entre seus parágrafos; preserve poemas e suas quebras reais.
- Título/subtítulo da folha de rosto próximos; autor e logo proporcionais. Alinhamento do logo à base é escolha do projeto, não justifica converter o livro inteiro em layout fixo. Confira aumento de fonte e leitores sem suporte ao layout usado.
- Dimensões relativas; evite posicionamento absoluto no fluxo, alturas fixas para texto e cor/fundo forçados. Letras continuam texto, não imagens.
- Imagens significativas com alt contextual; decoração com alt vazio. Retrato centrado e legenda depois. Capas e ilustrações preservam proporção.
- Catálogo somente se fornecido/solicitado: capítulo final distinto, título separado da grade, capas compactas e proporções preservadas; chamadas institucionais na ordem aprovada.

## Notas e fontes

Chamada aponta ao contêiner completo da nota (`aside` com `epub:type="footnote"`); mantenha vínculo de retorno. No perfil que adote notas justificadas, declare seu alinhamento explicitamente, sem recuo e com pequeno espaço entre notas. Título “Notas” depende da estrutura aprovada, não é acrescentado por padrão.

Chamada sobrescrita não deve aumentar entrelinha: tamanho relativo, `line-height:0`, deslocamento relativo e alinhamento baseline são uma opção a verificar no leitor. Preserve semântica e área clicável.

Incorpore OTF/TTF somente com autorização e licença compatível. Declare estilo/peso, fallback e confira carregamento real. Se a prévia não suportar ofuscação IDPF, decodifique só em memória ou use leitor compatível; não remova a proteção do arquivo entregue.

## Itálicos e nomes

Pesquise na internet a função contextual de cada termo a classificar: pessoa, lugar, instituição, tradição, termo estrangeiro, título ou ênfase. Priorize original, autoridades bibliográficas, museus, universidades e dicionários; uma fonte pode sustentar vários casos. Registre termo, classificação, estilo, contexto e URL. Não repita pesquisas já sustentadas.

No perfil editorial padrão, nomes próprios ficam em redondo, títulos de obras mencionados em itálico e estrangeirismos não incorporados em itálico. Um título inteiro permanece em itálico mesmo contendo nome pessoal. Dentro de ênfase discursiva, confira o nome separadamente. O projeto pode definir exceções justificadas.

Não herde itálicos cegamente, não remova todas as ênfases e não infira identidade pela grafia. Uniformize termos incorporados e tradições segundo um critério registrado; “Zen” designando a tradição fica em redondo nesse perfil. Converta negrito em itálico apenas quando solicitado, aplicando depois as exclusões de nomes.

Analise palavras completas através de span/em/strong: fragmentos de estilo não são fronteiras de palavra. Preserve limites de parágrafo e quebras reais. Se a pesquisa for inconclusiva, preserve o trecho, informe a dúvida e avance nos casos independentes confirmados.

## Auditoria somente de leitura

Crie um JSON de projeto no formato:

```json
{"terms":[{"text":"Zen","kind":"tradition","style":"roman","source":"https://www.shambhala.com/the-book-of-tea-3087.html"}]}
```

`kind`: person/place/institution/tradition/foreign/work. `style`: roman/italic. `source`: URL HTTP(S) da evidência consultada. Cadastre variantes separadamente; não reutilize lista de outro livro como classificação universal.

```bash
python3 scripts/editorial_audit.py LIVRO.epub registro.json
python3 scripts/editorial_audit.py LIVRO.epub registro.json --forbid-bold
python3 scripts/editorial_audit.py --self-test
```

O relatório apresenta tratamentos incorretos/parciais, contextos, contagens e termos mistos/não encontrados. Negrito é sinalizado somente com a opção correspondente. Saída 1 significa achados ou CSS a revisar; saída 0 não prova revisão completa. O auditor observa marcação e estilos inline, não calcula cascata CSS, não verifica a veracidade das fontes e não classifica termos novos. Confira estilos computados no leitor e avalie homônimos/ocorrências contextuais manualmente.

## Hifenização e romanos

Se o projeto excluir nomes e estrangeirismos da hifenização, não dependa de `hyphens:auto`. Use pontos U+00AD somente em palavras minúsculas reconhecidas por dicionários ortográfico e de hifenização do idioma. Exclua estrangeirismos, itálicos, links e código; pule palavras divididas entre estilos. Confira preservação removendo U+00AD da comparação.

Versaletes de romanos só quando previstos pelo perfil e sustentados pela fonte. Reconheça palavras completas; “I” + “mortalidade” não é um numeral. O helper incluído faz detecção conservadora e contém self-test.

## Conferência visual

Confira capa e avanço sem duplicação, preliminares, índice e menu, aberturas, corpo, citações, todas as figuras, notas ida/volta, final do livro, fonte ampliada e modo escuro. Use EPUBCheck para conformidade, auditor para escopo lexical e um leitor para aparência: eles respondem a perguntas diferentes.
