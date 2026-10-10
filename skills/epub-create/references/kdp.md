# Perfil Amazon KDP — EPUB refluível

Orientação conferida em 10 de outubro de 2026. Reabra as páginas oficiais antes de cada entrega KDP; requisitos mudam. Este projeto não tem vínculo com a Amazon.

## Navegação

Sumário visível no início, com links, sem páginas impressas e sem tabelas HTML usadas para disposição. Confira ordem e destinos. Inclua navegação lógica EPUB 3; no perfil KDP, preserve ou gere também NCX compatível com os mesmos destinos, conforme as recomendações oficiais. Landmarks de capa e sumário complementam a navegação. Não achate a hierarquia textual para contornar limites do menu.

Fonte: [Diretrizes de navegação](https://kdp.amazon.com/en_US/help/topic/GY3AD8C6C6GAG42N).

## Corpo, fontes e notas

Respeite ajustes de tamanho, entrelinha, fonte e cores do leitor. No corpo corrente, mantenha defaults e evite regras de font-size/line-height, margens/padding laterais gerais e cor/fundo impostos. Se incorporar fonte, configure a família principal no body sem forçá-la em cada parágrafo; títulos e elementos especiais podem ter tratamento próprio. Não deixe o corpo inteiro negrito/itálico.

Notas precisam de links de ida e retorno; prefira aside semântico contendo todo o texto, ao fim do capítulo/livro. Confira o conteúdo do pop-up. Remova páginas impressas do sumário; referências internas e índice remissivo precisam de destinos adequados. Real Page Numbers é mapeamento para edição física, não paginação refluível automática nem garantia de prévia local.

Fonte: [Texto refluível](https://kdp.amazon.com/en_US/help/topic/GH4DRT75GWWAGBTU).

## Capas

Distinga capa promocional enviada separadamente de capa interna. Confira a imagem interna e declaração OPF `cover-image`, sem duplicações após a conversão. Para a capa promocional, a orientação consultada recomenda JPEG RGB e 2560 × 1600 pixels; revalide as especificações atuais antes de exportar. Não use capa de impressão com lombada/contracapa como capa digital, não estique imagem insuficiente e confira título/autor contra os metadados. Não presuma suporte uniforme a SVG: a página oficial registra limitação no aplicativo para iPad.

Fonte: [Diretrizes de capa](https://kdp.amazon.com/en_US/help/topic/G6GTK3T3NUHKLEFX).

## Acessibilidade

Defina idioma, hierarquia, listas/tabelas semânticas, links descritivos e alternativas para imagens. Decoração não deve ser anunciada como conteúdo. Confira contraste nos temas e ordem de leitura. Não transforme tabelas ou texto em imagens por conveniência.

Fonte: [Diretrizes de acessibilidade](https://kdp.amazon.com/en_US/help/topic/GF9Z3HLUMTRJ6QPL).

## Portão de qualidade

Antes da entrega KDP, execute EPUBCheck, compare conteúdo e confira navegação/recursos. A página de QA consultada limita cada HTML a menos de 30 MB e o livro a menos de 300 HTMLs; revalide limites antes da entrega. Use Kindle Previewer para conversão, logs, navegação, notas, imagens, ajustes e temas; uma prévia EPUB.js não substitui esse teste. Se disponível, Ace by DAISY complementa a avaliação de acessibilidade.

Sem Kindle Previewer, entregue como EPUB validado com conferência Kindle pendente. Não envie o livro à KDP, não entre em conta e não prometa aprovação sem autorização e evidência.

Fonte: [Controle de qualidade](https://kdp.amazon.com/en_US/help/topic/GGRXLC5USU4H67YM). Índice oficial: [Diretrizes para publicação no Kindle](https://kdp.amazon.com/pt_BR/help/topic/GU72M65VRFPH43L6).
