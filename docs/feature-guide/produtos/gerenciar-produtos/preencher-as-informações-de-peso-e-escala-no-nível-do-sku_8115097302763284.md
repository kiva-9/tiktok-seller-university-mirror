---
title: "Preencher as informações de peso e escala no nível do SKU"
id: 8115097302763284
category: "Gerenciar produtos"
url: "https://seller-br.tiktok.com/university/essay?knowledge_id=8115097302763284"
update_time: "2026-09-30"
keywords: ""
---
### Detalhes das alterações

#### Escopo

|  |  |
| --- | --- |
| **Item** | **Descrição** |
| **Produtos aplicáveis** | Produtos com pelos menos dois SKUs. Produtos de SKU único continuam a usar informações no nível do produto |
| **Não compatível com esta fase** | Produtos de combo virtual (incluindo produtos de combo de mesmo conjunto) continuam a usar informações no nível do produto. O APP não é compatível com a criação/edição de dimensões e peso no nível do SKU |
| **Lógica padrão** | Por padrão, as dimensões e o peso ainda são inseridos no nível do produto (PID). Os vendedores devem marcar manualmente a opção a fim de alterar para o nível do SKU. |

#### Dimensões e peso no nível do SKU vs. Dimensões e peso no nível do produto

|  |  |  |
| --- | --- | --- |
| **Comparação** | **Nível do produto (PID) (antigo/padrão)** | **Nível do SKU (novidade)** |
| **Grau de detalhe das informações** | Um conjunto de dimensões e peso para o produto inteiro | Cada SKU tem sua própria dimensão e peso |
| **Exibição da taxa de envio no lado do consumidor** | Todos os SKUs do mesmo produto mostram a mesma taxa de envio | SKUs diferentes mostram as taxas de envio correspondentes e a taxa atualiza em tempo real quando os usuários trocam entre SKUs |
| **Cenários aplicáveis** | O tamanho/peso da embalagem geralmente é consistente entre SKUs | Diferentes especificações, combos ou capacidades criam diferenças significativas de pacote |
| **Há necessidade de ativação manual?** | Nenhuma ação necessária. Mantenha a experiência atual | É necessário ativar manualmente a opção Configurar peso e dimensões por SKU |

---

## Guia do recurso (por ponto de entrada)

> **Pré-requisitos**: o produto deve ter pelo menos dois SKUs; não deve ser um produto de combo virtual; e o mercado atual deve ter ativado as dimensões e o peso no nível do SKU.

#### Cenário 1: anúncio de novo produto

**Caminho**: **Central do vendedor → Produtos → Adicionar novo produto → Informações de venda → Lista de SKUs → Botão "Opções" → clique em "Peso e dimensões do SKU". Etapas**:  

1. Na página de novo produto, primeiro preencha as informações básicas padrão do produto e as informações do SKU (de pelo menos dois SKUs).
2. **Marque "Configurar peso e dimensões por SKU"** (opção desmarcada por padrão).

   ![image](https://p16-oec-university-sign-sg.ibyteimg.com/tos-alisg-i-nk3i2mqmvs-sg/250eea192dfb4efa92f3ce6fa2737234~tplv-nk3i2mqmvs-image.png?lk3s=5d1a069b&x-expires=2106124616&x-signature=79rREK%2FOba9Ki6JUPEwaSjxQ75c%3D)
3. Após a marcação:
   * Os campos de informações originais de dimensão e peso no nível do produto são ocultados automaticamente;
   * A lista de SKUs **adicionará novas colunas para peso/comprimento/largura/altura**.

     ![image](https://p16-oec-university-sign-sg.ibyteimg.com/tos-alisg-i-nk3i2mqmvs-sg/24b5fe5de39849208e62ac65f47366b8~tplv-nk3i2mqmvs-image.png?lk3s=5d1a069b&x-expires=2106124613&x-signature=J%2FJ%2BRTRjv%2FqJtHCW%2BOXhj564XoM%3D)
4. Na lista de SKUs, preencha as dimensões e o peso no nível do SKU usando qualquer um dos três métodos a seguir:
   * **Inserir individualmente**: insira os valores diretamente em cada linha de SKU;
   * **Aplicar em massa**: use a entrada **Aplicar em lote** no cabeçalho da tabela para preencher todos os SKUs de uma vez;
   * **Por dimensão em lote**: por exemplo, preencha por cor/tamanho para melhorar a eficiência.
5. Após concluir as informações, clique em **Enviar**.

**Dicas**

* Após a ativação do nível do SKU, os **campos de dimensão e peso no nível do produto não serão mais exibidos** e as informações de dimensão/peso seguirão as informações no nível do SKU.
* Se o produto tem apenas um SKU, continue a usar o nível do produto (PID), que é consistente com a experiência original.

#### Cenário 2: edição de produto

**Caminho**: **Central do vendedor → Produtos → Gerenciar produtos → Edite os produtos que deseja -> Informações de venda -> Lista de SKUs -> Botão "Opções" -> clique em "Peso e dimensões do SKU". Recursos compatíveis**:  

* **PID → SKU**: produtos existentes que originalmente usam informações no nível do produto podem ser alterados para usar informações no nível do SKU na página de edição, ao **marcar "Configurar peso e dimensões por SKU"** e complementar as dimensões e o peso para cada SKU.
* **SKU → PID**: para produtos que já usam informações no nível do SKU, apenas **desmarque** a opção a fim de reverter para o nível do produto (PID).
* **Edições no nível do SKU**: ajuste diretamente as dimensões e o peso de qualquer SKU na lista de SKUs e salve.
* A cadeia completa (lado do vendedor → logística → taxa de envio do lado do consumidor) será atualizada com base nos dados mais recentes.

**Antes da ativação (a seção de Informações de venda é padronizada para o nível do PID e a seção de Envio abaixo é usada para preencher as dimensões e o peso no nível do produto):**

![image](https://p16-oec-university-sign-sg.ibyteimg.com/tos-alisg-i-nk3i2mqmvs-sg/6184067f6c1242e9ba1e69f7f163da0d~tplv-nk3i2mqmvs-image.png?lk3s=5d1a069b&x-expires=2106124614&x-signature=AFssbhOIIZ3%2BjfNyCp%2F6n7Y36%2Fs%3D)

**Após a ativação (a seção de Informações de venda adiciona os campos de peso e dimensões de SKU necessários, enquanto as informações da seção de Envio são ocultadas):**

![image](https://p16-oec-university-sign-sg.ibyteimg.com/tos-alisg-i-nk3i2mqmvs-sg/9898a40512fd46c48df93c3697c1431f~tplv-nk3i2mqmvs-image.png?lk3s=5d1a069b&x-expires=2106124616&x-signature=TKUohbCAvWuJS%2FnBDduDXfT0%2B8U%3D)

![image](https://p16-oec-university-sign-sg.ibyteimg.com/tos-alisg-i-nk3i2mqmvs-sg/96df18b110d6462d9cb8a6a86e8a1791~tplv-nk3i2mqmvs-image.png?lk3s=5d1a069b&x-expires=2106124618&x-signature=9Vj2FlYOom4x3iQTRskap2321Rg%3D)

**Gerenciamento em massa: você pode preencher as dimensões e o peso para vários SKUs em uma única operação**

![image](https://p16-oec-university-sign-sg.ibyteimg.com/tos-alisg-i-nk3i2mqmvs-sg/5c642e6e8b50435eaf99e365a6d15e31~tplv-nk3i2mqmvs-image.png?lk3s=5d1a069b&x-expires=2106124614&x-signature=zw%2B3X8G0S3MsfKWSqKPiqDBuitY%3D)

![image](https://p16-oec-university-sign-sg.ibyteimg.com/tos-alisg-i-nk3i2mqmvs-sg/a1bd3c7ddc764e95b1dae285db974850~tplv-nk3i2mqmvs-image.png?lk3s=5d1a069b&x-expires=2106124615&x-signature=0FRJVwFTjCoHtbqUi4Vk8Z%2B9dhA%3D)

**Exclusividade mútua com combo (combo virtual): uma vez que as dimensões e o peso no nível do SKU são ativados, a opção Combo fica esmaecida**

![image](https://p16-oec-university-sign-sg.ibyteimg.com/tos-alisg-i-nk3i2mqmvs-sg/311cc44a7a964b028e8d5f94ccedd9f3~tplv-nk3i2mqmvs-image.png?lk3s=5d1a069b&x-expires=2106124614&x-signature=gHc6ULup%2FiWGnHqHSC%2BpMwFTMoY%3D)

![image](https://p16-oec-university-sign-sg.ibyteimg.com/tos-alisg-i-nk3i2mqmvs-sg/6a0beb0c018f4230923d1cabc9bb6b4b~tplv-nk3i2mqmvs-image.png?lk3s=5d1a069b&x-expires=2106124616&x-signature=uaDdhrKTZvcp4VZomjCe%2Fe4FEs8%3D)

**Observação**: ao trocar do nível do SKU para o nível do PID, os dados de dimensão e peso originais do nível do SKU serão substituídos por um conjunto unificado no nível do produto. Confirme antes de salvar.  

#### Cenário 3: anúncio em lote com o Excel

**Caminho**: Central do vendedor → Produtos → Anúncios em massa/edição em massa (modelo do Excel)   
**Etapas**:  

1. No modelo do Excel, insira os campos de **dimensão e peso** separadamente para **vários SKUs do mesmo produto**.
2. SKUs diferentes do mesmo produto devem ser inseridos em várias linhas, e diferentes valores são permitidos nas colunas de dimensão/peso.
3. Carregue o arquivo Excel e os dados serão importados assim que a plataforma os reconhecer com sucesso.
4. Após a importação, você poderá ver nos detalhes do produto que cada SKU foi associado com seus próprios dados de dimensão e peso.

**Modelo do Excel: uma linha por SKU, com diferentes valores de peso e dimensão inseridos por linha de SKU**

![image](https://p16-oec-university-sign-sg.ibyteimg.com/tos-alisg-i-nk3i2mqmvs-sg/9c17619f114d4a609a6fe323e5f864c4~tplv-nk3i2mqmvs-image.png?lk3s=5d1a069b&x-expires=2106124613&x-signature=tzDJoztP9m5YvpNK5CQnBGr4Suc%3D)

#### Cenário 4: APP (somente visualização, sem compatibilidade com criação/edição)

* Se um produto já foi configurado com dimensões e peso no nível do SKU no PC, o **APP solicitará que as dimensões e o peso do pacote devem ser editados no PC** e nenhuma edição de informação ficará disponível no APP.
* Se o produto ainda usa o nível do PID, a experiência de edição no APP permanece inalterada.

**Seção de envio no APP: quando o produto ativar as dimensões e o peso do SKU no PC, o módulo Peso e dimensões será ocultado. Apenas uma mensagem de orientação será exibida, direcionando os vendedores a editar o produto na Central do vendedor no PC.**

#### Cenário 5: integração de API/ISV (vendedores de API aberta)

* Os novos campos de dimensão e peso no nível do SKU são introduzidos nesta versão. **Se os vendedores carregam produtos por meio de APIs próprias ou ISVs**, o ISV deve concluir a integração dos novos campos antes que as dimensões e o peso no nível do SKU possam ser carregados.
* Se o ISV não concluiu a atualização, a API continuará a carregar por nível do produto (PID), sem afetar a existência da funcionalidade.
* Interfaces envolvidas: os campos serão atualizados na criação, carregamento e consulta do produto, além de em outras APIs relacionadas.
* **Horário de lançamento da API**: os campos serão publicados externamente após o recurso do PC do lado do vendedor ser lançado, e então os vendedores e ISVs podem começar a integração.

**Recomendação de integração de API**: vendedores usando ISVs são orientados a entrar em contato com os provedores de ISV assim que possível a fim de concluir a adaptação para os novos campos. Vendedores com integrações próprias devem seguir as atualizações na [Documentação de plataforma aberta](https://partner.tiktokshop.com/docv2/page/07q2huia "https://partner.tiktokshop.com/docv2/page/07q2huia").  

---

## Mudanças da experiência do lado do consumidor

* **Página de detalhes do produto/carrinho/finalização da compra**: quando os usuários trocarem entre SKUs diferentes, a **taxa de envio será calculada novamente em tempo real com base nas dimensões e no peso do SKU correspondente**, em vez de apresentar um valor unificado.
* Percepção do usuário: **o que você seleciona é o que você recebe** — as taxas de envio são claras e correspondem estritamente ao SKU selecionado.
* A IU geral do lado do consumidor permanece inalterada. Apenas a lógica por trás do cálculo da taxa de envio atualiza quando os usuários trocam entre SKUs.

**Alteração na estimativa da taxa de envio no lado do vendedor**: quando não há ativação das dimensões e do peso no nível do SKU, as taxas/custos de envio são exibidos como um valor estimado. Após a ativação das dimensões e do peso no nível do SKU, as taxas/custos de envio são exibidos como uma **faixa de preço** (já que diferentes SKUs têm diferentes valores de peso).   
**Alteração na estimativa da taxa de envio no lado do consumidor: as taxas de envio no lado do consumidor são exibidas com exatidão para diferentes SKUs com base nas dimensões e no peso no nível do SKU.**

---

## Ações necessárias por parte dos vendedores

1. **Avalie seu catálogo**: identifique produtos em que as dimensões/peso da embalagem tenham variações significativas entre SKUs e priorize a ativação da dimensão e do peso no nível do SKU para esses produtos.
2. **Ative passo a passo**: ao criar ou editar produtos no PC, ative manualmente a opção **Configurar peso e dimensões por SKU**.
3. **Valide os dados**: após inserir as informações, verifique a taxa de envio exibida na página de informações do produto do lado do usuário e certifique-se de que ela se alinha aos custos reais de logística.
4. **Atualize a integração de ISV**: se você carrega por meio de um ISV, confirme antecipadamente o cronograma para a integração dos novos campos com o seu provedor de ISV.

---

## Perguntas frequentes

|  |  |
| --- | --- |
| **Pergunta** | **Resposta** |
| Se eu não ativar o nível do SKU, os produtos existentes serão afetados? | Não. O padrão permanecerá o nível do produto (PID) e não haverá alterações nos produtos existentes. |
| Se eu já tiver inserido dados por SKU, posso trocar de volta para o nível do PID? | Sim. Apenas desmarque a opção na página de edição do produto no PC e a plataforma substituirá os dados com um conjunto unificado de dimensões e peso. |
| Produtos de combo virtual podem usar informações do nível do SKU? | Não nesta fase. Produtos de combo ainda usam informações de nível do produto e serão iterados separadamente depois. |
| Por que não posso editar as dimensões e o peso do SKU no APP? | Esse recurso não está disponível no APP nesta fase. Crie ou edite no PC. |
| Por que às vezes preciso complementar "Informações de logística" durante a distribuição para outros países? | Quando o país de destino ainda não ativou as dimensões e o peso no nível do SKU, um conjunto de dimensões e peso deve ser enviado no nível do produto. A plataforma preencherá valores sugeridos com base nos dados do SKU de origem, que podem ser editados e confirmados pelos vendedores. |
| O que precisa ser feito para a integração de API? | Novos campos relacionados às dimensões e ao peso no nível do SKU foram adicionados. Vendedores que usam ISVs precisam incentivar os ISVs a concluírem a integração dos campos. Vendedores com integrações próprias devem atualizar a lógica de acordo com a Documentação de plataforma aberta. |
