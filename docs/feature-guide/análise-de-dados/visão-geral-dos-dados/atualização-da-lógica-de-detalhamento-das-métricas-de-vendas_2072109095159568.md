---
title: Atualização da lógica de detalhamento das métricas de vendas
id: 2072109095159568
category: Visão geral dos dados
url: "https://seller-br.tiktok.com/university/essay?knowledge_id=2072109095159568"
update_time: 2026-04-28
keywords: Vendedores
---




# O que lançamos?

Atualizamos e unificamos a lógica de atribuição das métricas de vendas. Essa alteração garante uma metodologia consistente para **GMV, contagem de pedidos, itens vendidos e contagem de pedidos em nível de SKU** em todos os módulos de produto.

A **lógica de detalhamento do GMV** também foi atualizada:

* **Anteriormente:** o GMV era inicialmente dividido por **tipo de conteúdo** (LIVE, vídeo curto, cartão de produto) e, em seguida, por **tipo de conta** (conta vinculada vs. conta de afiliado).
* **Agora:** foi adicionado um novo detalhamento de vendas por **origem do pedido** (afiliado vs. vendedor), substituindo o detalhamento anterior por **tipo de conta** (conta de afiliado vs. conta vinculada), mantendo o detalhamento existente por tipo de conteúdo (LIVE, vídeo curto, cartão de produto).![whiteboard_exported_image (13).png](https://p16-oec-university-sign-sg.ibyteimg.com/tos-alisg-i-nk3i2mqmvs-sg/ccc20f85ad634a56843cae9ccb5615dc~tplv-nk3i2mqmvs-image.png?lk3s=5d1a069b&x-expires=2092165967&x-signature=jwcJZmeofbHPNLO%2B59kRKrxuIa8%3D)

Com a lógica de atribuição atualizada, os comerciantes podem obter uma compreensão mais clara de como diferentes formatos de conteúdo contribuem para as vendas. Para refletir o impacto total do conteúdo, as vendas são categorizadas como **Diretas e Indiretas**. As Diretas capturam as conversões imediatas impulsionadas pelo conteúdo; as Indiretas capturam as compras posteriores influenciadas pelo conteúdo.

|  |  |
| --- | --- |
| **GMV direto** | **GMV indireto** |
| Refere-se às vendas geradas quando um usuário **conclui uma compra diretamente enquanto interage com o conteúdo**.  **Exemplo:**  O usuário assiste a um vídeo curto com um link para o produto, clica no link, adiciona o produto ao carrinho e conclui a compra. Este pedido será atribuído à **parcela direta do GMV de vídeos**. | Refere-se às vendas geradas quando um usuário **interage com o conteúdo e visualiza o produto relacionado, mas conclui a compra posteriormente, em um determinado período**. Esses pedidos refletem a **influência tardia do conteúdo**.  **Exemplo:**  Um usuário assiste a um vídeo com um link de produto e clica no produto, mas não realiza a compra imediatamente. Dentro de 1 dia, o usuário busca o produto no TikTok Shop e conclui a compra. Esse pedido será atribuído como **GMV indireto de Vídeo**. |

![image](https://p16-oec-university-sign-sg.ibyteimg.com/tos-alisg-i-nk3i2mqmvs-sg/ba750b42c3b1496188dac75627bfb7fc~tplv-nk3i2mqmvs-image.png?lk3s=5d1a069b&x-expires=2092165954&x-signature=LouPOqNjVVmxo8a3Qft4TfeVKNg%3D)

**A mesma lógica de atribuição também se aplica a outros formatos de conteúdo.**

# Por que lançamos isso?

Anteriormente, em diferentes produtos de análise, havia várias maneiras de detalhar as vendas, incluindo afiliado vs. vendedor e LIVE vs. vídeo vs. cartão de produto. No entanto, esses diferentes métodos não podem ser referenciados de forma cruzada. Por exemplo, anteriormente, o GMV atribuído à LIVE do afiliado podia não corresponder à mesma métrica na Central do vendedor.  
Embora cada lógica de atribuição tivesse sua justificativa, ela não sustentava uma visão holística do desempenho do negócio. Com o novo lançamento, é possível ver claramente a contribuição de cada componente.  
E, para as métricas relacionadas a vendas, aprimoramos a dica da ferramenta para explicar melhor o impacto direto e indireto, além da explicação da própria métrica.  

# Quais produtos foram impactados por esse lançamento?

As métricas relacionadas a vendas, como GMV, pedidos, pedidos por SKU, itens vendidos e métricas relacionadas, como GPM, CTOR (taxa de cliques para pedidos), estão disponíveis na Central do vendedor, Central de afiliados, Central de criadores, Gerenciador de LIVE, Painel de LIVE, aplicativo do vendedor, Central de parceiros e API aberta.  
Você poderá notar que, em comparação com o **GMV de LIVE anterior e o GMV de vídeos, o GMV atribuído a transmissões ao vivo e o GMV atribuído a vídeos foram alterados.** Isso já era esperado, visto que, anteriormente, o GMV de transmissões ao vivo e de vídeos não considerava o impacto indireto.  

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| Central do vendedor - análises da loja | Central do vendedor - vídeo | Central do vendedor - LIVE | Central do vendedor - produto | Aplicativo do Central do vendedor |
| image | image | image | image | image |

# Como você pode usar essas métricas para analisar o desempenho do seu negócio?

Você pode analisar o desempenho do seu negócio por origem do pedido ou por tipo de conteúdo.  
A origem do pedido indicará se o GMV é gerado pela contribuição de criadores afiliados. Você pode obter mais informações sobre a contribuição de cada tipo de conteúdo. Por exemplo, quanto foi gerado pelos vídeos dos criadores afiliados. Em cada tipo de conteúdo, você pode descobrir quanto da receita é proveniente de clientes que fizeram um pedido diretamente a partir do vídeo com produtos à venda ou das transmissões ao vivo.  
O tipo de conteúdo indicará a parcela do GMV gerada por cada tipo de conteúdo. Por exemplo, quanto é gerado por vídeos com produtos à venda ou transmissões ao vivo. Você também pode saber qual é a contribuição dos criadores afiliados. Assim, você saberá quanto é proveniente de clientes que fizeram pedidos diretamente a partir dos vídeos com produtos à venda ou das transmissões ao vivo. Você pode escolher a abordagem que melhor se adapta ao seu caso de uso.  
![whiteboard_exported_image (14).png](https://p16-oec-university-sign-sg.ibyteimg.com/tos-alisg-i-nk3i2mqmvs-sg/45d0f8b92c964a2ba43bd93be5c23818~tplv-nk3i2mqmvs-image.png?lk3s=5d1a069b&x-expires=2092165992&x-signature=%2B7sbNNHNsixgEJHI3%2BiyCuL%2F1kw%3D)![whiteboard_exported_image (15).png](https://p16-oec-university-sign-sg.ibyteimg.com/tos-alisg-i-nk3i2mqmvs-sg/c967df2500724ded8c6720f464dccf96~tplv-nk3i2mqmvs-image.png?lk3s=5d1a069b&x-expires=2092165996&x-signature=pP%2B%2BATh7zc%2B53kwbkUfbQ5VRZoE%3D)

# Perguntas frequentes

1. Não, isso não afetará a taxa de comissão.

1. Não, ele não afeta o seu GMV total, apenas altera a forma como o GMV é alocado entre os segmentos.

1. Não, ele não afetará quanto dinheiro você ganha. Apenas alterou a forma de distribuir o GMV em diferentes segmentos.

1. Sim, disponibilizaremos os dados usando essa nova lógica de atribuição para dados históricos acessíveis. Se você quiser comparar o número com os dados fornecidos antes de usar a lógica de atribuição original, pode consultar a parte direta da métrica. Pode haver ligeiras diferenças, o que é esperado.

1. Isso é esperado. O GMV representa o valor total pago pelos clientes naquele dia. O pedido poderia ser atendido por meio de um vídeo assistido pelo cliente no período de 7 dias. Portanto, é possível que, mesmo que naquele dia nenhum vídeo tenha sido publicado ou visualizado, você tenha um GMV atribuído a vídeos.

1. O pedido foi feito **no período de 7 dias após a visualização da LIVE do afiliado (3 de abril)**.
2. A **LIVE do afiliado foi o último conteúdo deste vendedor que o usuário visualizou**.
3. Portanto, de acordo com a **lógica de atribuição de último toque**, o pedido é atribuído à categoria **Afiliado – GMV indireto**.

1. **Este lançamento afetará o valor da minha comissão de afiliado?**
2. **Este lançamento afetará o GMV que gerei?**
3. **Esse lançamento afetará meus ganhos?**
4. **Este lançamento afetará os dados históricos?**
5. **Por que ainda posso ter GMV atribuído a vídeos mesmo sem ter publicado nenhum vídeo naquele dia?**
6. Se um usuário assistiu a um **vídeo de afiliado em 1º de abril**, a uma **LIVE de vendedor em 2 de abril** e, em seguida, a uma **LIVE de afiliado em 3 de abril**, *(\*Para que uma interação com o conteúdo seja considerada na atribuição, o usuário deve* ***assistir ao vídeo ou à LIVE e clicar no link do produto****. Se o usuário apenas assistir ao conteúdo, mas* ***não clicar no link do produto****, essa interação será ignorada na atribuição)* e, finalmente, fez um pedido em **9 de abril pela aba Loja**, de acordo com a lógica de detalhamento recém-atualizada, o pedido será atribuído à categoria **Afiliado – GMV indireto**. Isso porque:
