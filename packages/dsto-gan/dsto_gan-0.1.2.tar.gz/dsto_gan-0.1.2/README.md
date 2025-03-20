# DSTO-GAN: Balanceamento de Dados com GAN

O **DSTO-GAN** é uma biblioteca Python que utiliza uma Rede Generativa Adversarial (GAN) para gerar amostras sintéticas e balancear datasets desbalanceados. Ele é especialmente útil para problemas de classificação em que as classes estão desproporcionais.

---

## Funcionalidades

1. **Geração de amostras sintéticas** para balanceamento de classes.
2. **Treinamento de um GAN personalizado** para dados tabulares.
3. **Salvamento do dataset balanceado** em um arquivo `.csv`.

---

## Pré-requisitos

- **Python 3.7 ou superior**.
- **Gerenciador de pacotes `pip`**.


## Instalação

Você pode instalar a biblioteca diretamente via `pip`:

```bash
pip install dsto-gan
```

### Dependências

As dependências serão instaladas automaticamente durante a instalação. Caso prefira instalar manualmente, execute:

```bash
pip install numpy torch pandas scikit-learn xgboost scikit-optimize
```


## Como Usar

### 1. Preparação do Arquivo de Dados

O arquivo de entrada deve ser um `.csv` com a seguinte estrutura:
- A **última coluna** deve conter os rótulos das classes.
- As demais colunas devem conter as features (atributos) do dataset.

Exemplo de arquivo `desbalanceado.csv`:

```csv
feature1,feature2,feature3,class
1.2,3.4,5.6,0
2.3,4.5,6.7,1
3.4,5.6,7.8,0
```

### 2. Execução do Código

Salve o código em um arquivo Python, por exemplo: `gerar_balanceado.py`.

```python
from dsto_gan import process_data

# Caminhos dos arquivos de entrada e saída
input_file = "caminho/para/desbalanceado.csv"
output_file = "caminho/para/balanceado.csv"

# Processar o dataset e gerar o arquivo balanceado
process_data(input_file, output_file)

print(f"Dataset balanceado salvo em: {output_file}")
```

Execute o código no terminal:

```bash
python gerar_balanceado.py
```

### 3. Resultado

Após a execução, o programa gerará um arquivo `.csv` balanceado no caminho especificado. O arquivo de saída terá a mesma estrutura do arquivo de entrada, mas com as classes balanceadas.

---

## Exemplo de Uso

### Passo a Passo

1. Prepare o arquivo `desbalanceado.csv` com a estrutura correta.
2. Execute o código:
   ```bash
   python gerar_balanceado.py
   ```
3. Verifique o arquivo `balanceado.csv` gerado.

---

## Estrutura do Projeto

```
dsto_gan/
│
├── dsto_gan/          # Pacote principal
│   ├── __init__.py    # Inicialização do pacote
│   ├── dsto_gan.py    # Código principal para balanceamento de dados
├── setup.py           # Configuração do pacote
├── README.md          # Documentação do projeto
└── LICENSE            # Licença do projeto
```

---

## Solução de Problemas

### Erro ao Ler o Arquivo
- Verifique se o caminho do arquivo está correto.
- Certifique-se de que o arquivo está no formato `.csv` e segue a estrutura esperada.

### Erro de Instalação de Bibliotecas
- Certifique-se de que o `pip` está instalado e atualizado.
- Execute manualmente a instalação das bibliotecas:
  ```bash
  pip install numpy torch pandas scikit-learn xgboost scikit-optimize
  ```

### Erro Durante a Execução
- Verifique se o arquivo de entrada contém uma coluna de classes.
- Certifique-se de que todas as colunas, exceto a última, contêm valores numéricos.

---

## Contribuição

Contribuições são bem-vindas! Siga os passos abaixo:

1. Faça um fork do repositório.
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`).
3. Commit suas mudanças (`git commit -m 'Adicionando nova feature'`).
4. Faça push para a branch (`git push origin feature/nova-feature`).
5. Abra um Pull Request.

---

## Licença

Este projeto está licenciado sob a **Licença MIT**. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## Contato

- **Autor**: Erika Assis
- **Email**: dudabh@gmail.com
- **Repositório**: [GitHub](https://github.com/erikaduda/dsto_gan)

---

## Agradecimentos

Este projeto foi desenvolvido como parte de uma pesquisa em balanceamento de dados usando GANs. Agradecimentos à comunidade de código aberto por fornecer as bibliotecas utilizadas.
