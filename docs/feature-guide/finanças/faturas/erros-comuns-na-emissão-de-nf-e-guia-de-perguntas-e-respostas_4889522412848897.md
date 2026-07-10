---
title: Erros comuns na emissão de NF-e - Guia de Perguntas e Respostas
id: 4889522412848897
category: Faturas
url: "https://seller-br.tiktok.com/university/essay?knowledge_id=4889522412848897"
update_time: 2026-06-02
keywords: Vendedores
---




## **Possíveis erros da ferramenta de emissão de NF-e no TikTok Shop Brasil**

Alguns vendedores que usam a ferramenta de emissão de NF-e do TikTok Shop Brasil podem se deparar com mensagens de erro ao tentar emitir uma nota fiscal, semelhantes ao exemplo abaixo:

![image](https://p16-oec-university-sign-sg.ibyteimg.com/tos-alisg-i-nk3i2mqmvs-sg/7eb75a4395a042689ecd39f03e4a6b44~tplv-nk3i2mqmvs-image.png?lk3s=5d1a069b&x-expires=2069719557&x-signature=zsArg%2FyJVRyR5gUH6ME504AAbAo%3D)

Neste artigo, listamos os possíveis códigos de erro, explicamos as causas e sugerimos possíveis soluções ou o melhor curso de ação para resolvê-los.

Para localizar rapidamente um erro específico, use a função de pesquisa do navegador (ou o atalho Ctrl+F no teclado) e digite o código de erro que você está procurando.

### **Erro 33001017 - No processo de emissão de nota fiscal**

O pedido atual já está em processo de emissão de nota fiscal. Aguarde um momento e tente emitir a nota fiscal novamente mais tarde, pois o sistema já está processando a NF-e desse pedido.

### **Erro 33013001 - Número de série da NF-e inválido**

A Série é um código de até três dígitos usado para identificar um grupo de notas fiscais emitidas pelo mesmo estabelecimento. Ela ajuda a fazer a distinção entre vários tipos de seguros ou sistemas. Esse erro indica que o campo "Série" foi preenchido incorretamente. Ele deve conter um valor numérico entre 1 e 999.

**Como corrigir isso?**

1. Acesse **Minha conta > Configurações > Informações fiscais** na Central do vendedor TikTok Shop.
2. Certifique-se de que o campo "Série" contenha apenas números no intervalo de 1 a 999.
3. Salve a correção e recrie a NF-e.

### **Erro 33013002 - CST-PIS/COFINS inválido**

O CST é um código de classificação fiscal brasileiro usado para definir como um produto ou serviço é tributado nos sistemas federal (PIS, COFINS, IPI), estadual (ICMS) e municipal. Especificamente para PIS e COFINS, o CST determina como essas contribuições se aplicam a cada transação, com base na natureza do produto e no regime tributário da sua empresa.

Esse erro ocorre quando o CST-PIS/COFINS (Código de Situação Tributária) atribuído ao produto está ausente ou é inválido. Para resolver o problema, acesse a página de informações do produto na Central do vendedor TikTok Shop e atualize o campo CST. Certifique-se de que o Código de Situação Tributária do PIS e da COFINS seja válido e reflita corretamente o status fiscal do seu produto.

### **Erro 33013003 - CFOP inválido ou ausente**

O **CFOP** (Código Fiscal de Operações e Prestações) é um código fiscal de quatro dígitos usado em notas fiscais eletrônicas (NF-e) para classificar o tipo de transação, como vendas, devoluções, transferências, importações ou exportações.

Cada código CFOP corresponde a um tratamento fiscal específico e é essencial para gerar relatórios precisos para a SEFAZ.

Para resolver esse problema, acesse a página de informações do produto na Central do vendedor TikTok Shop e verifique se o CFOP está preenchido corretamente, se é um número válido de quatro dígitos e corresponde à natureza da transação (por exemplo, venda, devolução, transferência interestadual). Se você não tiver certeza de qual código CFOP usar, consulte seu consultor fiscal.

### **Erro 33013004 - Valor faturado inválido**

O valor total da nota fiscal é negativo, o que não é permitido. Verifique o valor do pedido e certifique-se de que o total seja maior que zero. Corrija e recrie a NF-e.

### **Erro 33013005 - Número de CNPJ inválido**

O CNPJ fornecido é inválido. Um CNPJ válido deve ser um número de 14 dígitos atribuído pela Receita Federal do Brasil quando a empresa é estabelecida.

### **Erro 33013006 - Código CEST inválido ou ausente**

O CEST (Código Especificador da Substituição Tributária) é um código de sete dígitos usado para identificar se um produto ou serviço se enquadra no sistema de substituição tributária do Brasil para PIS/COFINS. Esse erro ocorre quando o sistema detecta que o código CEST de um determinado produto está ausente ou é inválido.

Para resolver esse problema, certifique-se de que um código CEST de sete dígitos válido seja fornecido para o produto. Você pode verificar a validade do código CEST no [site oficial da SEFAZ](https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/legislacao/tipi-tabela-de-incidencia-do-imposto-sobre-produtos-industrializados "https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/legislacao/tipi-tabela-de-incidencia-do-imposto-sobre-produtos-industrializados").

### **Erro 33013007 - Código NCM inválido ou ausente**

A NCM (Nomenclatura Comum do Mercosul) é um sistema de classificação de oito dígitos usado no Brasil para desembaraço aduaneiro, cálculo de tarifas e declaração de impostos. Ela funciona de forma semelhante ao código internacional HS (Sistema Harmonizado) e é necessário para uma conformidade fiscal precisa.

Esse erro aparece quando o código NCM fornecido para um produto está ausente ou é inválido. Para corrigir o problema, certifique-se de que um código NCM válido de oito dígitos seja atribuído ao produto. Você pode verificar o código NCM correto usando o [banco de dados da SEFAZ](https://www4.receita.fazenda.gov.br/simulador/ "https://www4.receita.fazenda.gov.br/simulador/").

### **Erro 33013008 - O certificado digital expirou**

O certificado digital da empresa expirou e a emissão da NF-e não pode prosseguir. Atualize seu certificado digital na seção Informações fiscais da página Configurações da conta.

### **Erro 33013009 - CPF do comprador inválido**

Esse erro ocorre quando o número do CPF (Cadastro de Pessoas Físicas) fornecido pelo comprador é inválido. Como o CPF é um número de identificação de contribuinte obrigatório para pessoas físicas no Brasil, é necessário um CPF válido para a emissão da NF-e. Para resolver isso, entre em contato com o comprador e solicite que ele forneça um CPF válido.

### **Erro 33013010 - CNPJ não registrado**

Esse erro indica que o número do CNPJ (Cadastro Nacional da Pessoa Jurídica) associado à sua empresa não está registrado na SEFAZ (Secretaria da Fazenda). Para resolver isso, verifique o status de registro do seu CNPJ junto à SEFAZ.

### **Erro 33013011 - FCI inválida**

A FCI (Ficha de Conteúdo de Importação) é um documento obrigatório no Brasil usado para declarar a origem e o conteúdo de produtos importados, especialmente para fins relacionados à substituição tributária do ICMS. Esse erro indica que a FCI fornecida para o produto atual está ausente ou é inválida.

Acesse a página de informações do produto e verifique se o código FCI correto foi inserido. Após atualizar os detalhes do produto com a FCI válida, você pode recriar a NF-e.

### **Erro 33013012 - Regime tributário inconsistente fornecido**

O regime tributário indicado em sua NF-e não corresponde ao regime registrado na SEFAZ (Autoridade Tributária Brasileira).

No Brasil, as empresas devem declarar seu regime tributário (por exemplo, *Simples Nacional*, *Lucro Presumido* ou *Lucro Real*) ao se registrarem na SEFAZ. Esse regime tributário determina como a sua empresa será tributada e afeta diretamente a forma como as notas fiscais eletrônicas (NF-e) são validadas. Se o regime tributário utilizado na emissão da NF-e for diferente do oficialmente registrado, a nota fiscal será rejeitada.

Acesse a página Configurações da conta > Informações fiscais e confirme se o regime tributário selecionado corresponde ao registrado na SEFAZ. Se você não tiver certeza sobre seu regime tributário, entre em contato com seu contador ou verifique seus detalhes de registro no portal da SEFAZ.

### **Erro 33013013/33013014 - Código CFOP inválido para o tipo de operação**

O código CFOP (Código Fiscal de Operações e Prestações) fornecido não corresponde ao formato esperado para o tipo de operação (entrada ou saída).

O CFOP é um código fiscal de quatro dígitos usado para classificar a natureza das transações de mercadorias ou serviços para fins tributários no Brasil.

* Para **operações de entrada**, como compras e importações, o CFOP deve começar com **1**, **2** ou **3**.
* Para **operações de saída**, como vendas e exportações, o CFOP deve começar com **5**, **6** ou **7**.

O uso de um prefixo CFOP incorreto pode levar a problemas de cálculo de impostos (por exemplo, ICMS ou IPI) ou rejeição pela SEFAZ.

Analise o código CFOP atribuído ao seu produto e verifique se ele corresponde ao tipo correto de transação. Se necessário, consulte seu contador para obter a classificação de CFOP adequada.

### **Erro 33013015 - CFOP inválido para transação intraestadual**

Esse pedido é classificado como uma transação no mesmo estado, mas o código CFOP fornecido corresponde a uma operação interestadual.

O código CFOP usado está incorreto para uma transação intraestadual (no mesmo estado). Substitua o código CFOP por um que represente corretamente uma transação intraestadual e recrie a NF-e.

### **Erro 33013016 - O CFOP não corresponde ao código CST**

Cada código CST está associado a regras tributárias específicas e deve ser usado com um CFOP compatível. O uso de uma combinação incompatível pode resultar em rejeição pela SEFAZ.

O código CFOP fornecido não está alinhado ao CST (Código de Situação Tributária para PIS e COFINS) correspondente. Substitua o código CFOP por um que corresponda ao CST fornecido.

### **Erro 33013017 - Código EAN/GTIN inválido**

O EAN ou GTIN (Global Trade Item Number) é um código de barras padronizado de 13 dígitos usado para identificar exclusivamente produtos em transações comerciais. A SEFAZ valida esse código com base no registro nacional. Se o GTIN do produto não for encontrado ou estiver formatado incorretamente, a NF-e será rejeitada.

Certifique-se de que o código EAN/GTIN contenha exatamente 13 dígitos e esteja devidamente registrado no banco de dados nacional de GTIN da SEFAZ (Cadastro Centralizado de GTIN - CCG).

### **Erro 33013018 - O EAN/GTIN é inconsistente com a NCM.**

O código GTIN/EAN fornecido para o produto não está alinhado ao formato ou categoria esperado definido pela NCM (Nomenclatura Comum do Mercosul). A NCM é usada para classificação fiscal. A SEFAZ valida se o GTIN é apropriado para a NCM declarada.

Verifique se o código GTIN/EAN inserido para o produto contém exatamente 13 dígitos e corresponde à classificação NCM do produto. Se houver uma incompatibilidade, atualize o GTIN para um que seja válido e devidamente registrado sob a NCM correspondente no banco de dados nacional de GTIN (CCG).

### **Erro 33013019 - O EAN/GTIN é inconsistente com a CEST.**

O GTIN, comumente chamado de EAN-13, fornecido para o produto não corresponde ao valor esperado associado ao CEST (Código Especificador da Substituição Tributária) declarado. A SEFAZ verifica se o GTIN é válido para o código CEST específico.

Certifique-se de que o GTIN/EAN inserido para o produto seja um número válido de 13 dígitos e corresponda ao valor de GTIN esperado para o CEST selecionado. Se houver uma incompatibilidade, substitua-o por um GTIN válido devidamente registrado e associado ao CEST no banco de dados nacional de GTIN (Cadastro Centralizado de GTIN - CCG).

### **Erro 33013020 - Janela de tempo de cancelamento da NF-e excedida.**

De acordo com os regulamentos da SEFAZ, cada NF-e deve ser cancelada em um prazo específico após a emissão. Esse erro indica que o prazo para cancelamento já passou.

A NF-e não pode mais ser cancelada pelo processo padrão. Se for necessário reverter a transação, recomendamos que você emita uma NF-e de devolução, seguindo os procedimentos apropriados para devoluções.

### **Erro 33013021 - A NF-e não pode ser cancelada**

Quando uma NF-e é associada a um CTe (Conhecimento de Transporte Eletrônico), o cancelamento não é mais permitido de acordo com as normas da SEFAZ. O CTe serve como documento oficial de transporte. Sua vinculação à nota fiscal finaliza o processo da NF-e.

### **Erro 33013022 - Erro do sistema**

Erro do sistema - ocorreu um problema inesperado. Tente novamente mais tarde. Se o problema persistir, entre em contato com o suporte ao comerciante do TikTok Shop para obter assistência.

### **Erro 33013023 - O vendedor precisa concluir o processo de credenciamento para emissão de NF-e junto à SEFAZ do seu estado**

Este erro significa que o emissor **ainda não está autorizado pela SEFAZ a emitir Notas Fiscais Eletrônicas (NF-e)**.  
Isso pode ocorrer em situações como:  

* Empresas recém-criadas que ainda não concluíram o processo de credenciamento junto à SEFAZ;
* Empresas que já possuíam autorização anteriormente, mas que atualmente possuem pendências junto à SEFAZ ou à Receita Federal.

### **Erro 33013024 - Número de Série duplicado e já utilizado em outro lugar**

Acesse **Informações fiscais** e altere o **Número de Série da NF-e** para um número que não esteja sendo utilizado em outros lugares.  

### **Erro 33013025 - CFOP da NF-e inválido para MEI**

Acesse **Informações do produto** e altere o campo **CFOP** para um CFOP válido para MEI.  

### **Erro 33013026 - CSOSN da NF-e inválido para MEI**

Acesse **Informações do produto** e altere o campo **CSOSN** para um valor válido.  

### **Erro 33013028 - IE inválida**

Acesse **Informações fiscais** e altere a **IE (Inscrição Estadual)** para uma IE válida.  

### **Erro 33013029 - O certificado A1 enviado não corresponde ao CNPJ da empresa**

Acesse **Informações fiscais** e atualize o **Certificado A1** para um certificado vinculado ao mesmo CNPJ.  

### **Erro 33013030 - Tentativas de emissão de NF-e temporariamente bloqueadas pela SEFAZ**

As tentativas de emissão de NF-e foram temporariamente bloqueadas pela SEFAZ devido a envios inválidos repetidos ou em excesso.  
 Corrija o erro que causou as rejeições anteriores antes de reenviar a nota fiscal.  
 ⏳ Aguarde até **24 horas** antes de tentar novamente.  

### **Erro 33009001 - Status da nota fiscal atualizado.**

O status da nota fiscal do pedido atual já foi atualizado. Atualize a página e tente novamente.

### **Erro 33009007 - Informações fiscais ausentes**

Faltam informações fiscais do produto, o que impede a emissão da NF-e. Acesse a página do produto e preencha as informações fiscais necessárias para o item. Quando terminar, recrie a NF-e.
