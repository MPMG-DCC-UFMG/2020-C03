# C03
Coleta e tratamento de imagens de endereços

O código-fonte da ferramenta foi desenvolvido com a utilização da linguagem de programação Python 3. A versão atualizada do código-fonte encontra-se disponível no repositório do projeto no seguinte link: https://github.com/MPMG-DCC-UFMG/C03. Para realizar o download é necessário primeiro executar o comando:
`git clone https://github.com/MPMG-DCC-UFMG/C03.git`

Em tal repositório estão disponíveis os seguintes arquivos source:
- **main.py:** arquivo principal para a execução da ferramenta. Após a devida definição dos parâmetros necessários, esse arquivo tem a função de chamar os demais módulos para a execução da ferramenta. 
- **downloadData.py:** esse módulo é responsável para estabelecer a comunicação entre a ferramenta desenvolvida e as APIs utilizadas para o download das imagens, que no caso foram definidas o Google Maps e Google Street-View. Esse módulo implementa uma classe chamada Downloader que é responsável por lidar com as requisições de download das imagens. Caso, futuramente, outras APIs de coleta sejam incluídas no framework apenas uma encapsulação dessas APIs similar a classe Dowloader precisa ser implementada para manter o funcionamento da ferramenta.
- **io_handler.py:** realiza a leitura e escrita dos JSONs no formato previamente discutido.
- **sknet.py:** módulo que contém a implementação da rede neural Selective Kernels Networks e a função que realiza a inferência das imagens a partir do modelo previamente carregado.

É importante mencionar que os modelos da SKNet treinados (com experimentos relatados no relatório C03.2) estão disponível na VM cujo o acesso nos foi disponibilizado. Os arquivos dos modelos estão localizados na pasta models.

Preparação do ambiente utilizando o PIP:
No repositório do projeto, existe um arquivo denominada requirements.txt. Esse arquivo contém uma lista de todas as bibliotecas e suas devidas versões, que são necessárias para a execução da ferramenta. Logo para instalar todos esses módulos, basta usar o comando:

`pip install -r [path to requirments.txt]`

Execução do código para download e classificação das imagens 
`python3 main.py [parâmetros]`

Sendo os parâmetros:

Parâmetro | Tipo | Descrição
----------|------|------------
--google_maps_key | string | String contendo a chave da API do Google Maps.
--google_sview_key | string | String contendo a chave da API do Google Street-View.
--input_file | string |String com o caminho até o arquivo JSON de entrada. 
--output_path | string | String com o caminho em que serão salvos as imagens baixadas e o JSON com as predições.
--aerial_model | string | String com o caminho do arquivo para o modelo de classificação de imagens aéreas. 
--ground_model | string | String com o caminho do arquivo para o modelo de classificação de imagens térreas. 
--output_file | string |Nome do arquivo JSON que conterá as saídas do modelo de classificação.
--mode | string | **Opcional**. Esse parâmetro define o modo como a ferramenta será utilizada. Existem três valores possíveis para esse parâmetro: <ul><li>_complete_: (Valor padrão) a ferramenta executa todo o processo, isto é, recebe a lista de endereços, coleta as imagens, e classifica cada uma das localizações.</li><li>_download_: a ferramenta recebe a lista de localizações e, apenas, coleta as imagens.</li><li>_classify_: a ferramenta recebe uma lista de imagens(ver seção 3.2) e classifica cada uma das entradas.</li>  


