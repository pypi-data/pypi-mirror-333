import numpy as np
import torch
import torch.nn as nn
import pandas as pd
from torch.utils.data import DataLoader, TensorDataset

# Definir argumentos para o modelo
args = {
    'dim_h': 64,
    'n_z': 10,
    'lr': 0.0002,
    'epochs': 100,
    'batch_size': 64,
    'save': True,
    'train': True
}

# Verificar dispositivo (CPU ou GPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Modelos GAN
class Encoder(nn.Module):
    def __init__(self, args, num_input_features):
        super(Encoder, self).__init__()
        self.fc1 = nn.Linear(num_input_features, args['dim_h'])
        self.fc2 = nn.Linear(args['dim_h'], args['dim_h'])
        self.fc_mean = nn.Linear(args['dim_h'], args['n_z'])
        self.fc_logvar = nn.Linear(args['dim_h'], args['n_z'])
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        return self.fc_mean(x), self.fc_logvar(x)

class Decoder(nn.Module):
    def __init__(self, args, num_input_features):
        super(Decoder, self).__init__()
        self.fc1 = nn.Linear(args['n_z'], args['dim_h'])
        self.fc2 = nn.Linear(args['dim_h'], args['dim_h'])
        self.fc_output = nn.Linear(args['dim_h'], num_input_features)
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        return self.fc_output(x)

class Discriminator(nn.Module):
    def __init__(self, num_input_features):
        super(Discriminator, self).__init__()
        self.fc1 = nn.Linear(num_input_features, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, 1)
        self.relu = nn.ReLU(inplace=True)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        return self.sigmoid(self.fc3(x))

def G_SM1(X, y, n_to_sample, cl, encoder, decoder, args):
    # Gera amostras sintéticas usando o GAN
    X_tensor = torch.tensor(X, dtype=torch.float32).to(device)
    y_tensor = torch.tensor(y, dtype=torch.long).to(device)
    dataloader = DataLoader(TensorDataset(X_tensor, y_tensor), batch_size=args['batch_size'], shuffle=True)

    synthetic_data = []
    for _ in range(n_to_sample):
        z = torch.randn(1, args['n_z']).to(device)
        synthetic_sample = decoder(z).detach().cpu().numpy()
        synthetic_data.append(synthetic_sample)

    synthetic_data = np.vstack(synthetic_data)
    synthetic_labels = np.array([cl] * n_to_sample)
    return synthetic_data, synthetic_labels

def calculate_n_to_sample(y):
    class_counts = np.bincount(y)
    major_class_count = np.max(class_counts)
    n_classes = len(class_counts)
    n_to_sample_dict = {cl: major_class_count - class_counts[cl] for cl in range(n_classes)}
    return n_to_sample_dict, major_class_count

def train_gan(encoder, decoder, discriminator, X_train, args):
    optimizer_g = torch.optim.Adam(list(encoder.parameters()) + list(decoder.parameters()), lr=args['lr'])
    optimizer_d = torch.optim.Adam(discriminator.parameters(), lr=args['lr'])
    criterion_g = nn.MSELoss()
    criterion_d = nn.BCELoss()

    dataloader = DataLoader(torch.tensor(X_train, dtype=torch.float32), batch_size=args['batch_size'], shuffle=True)

    for epoch in range(args['epochs']):
        for batch in dataloader:
            # Configurar dados
            batch = batch.to(device)
            real_labels = torch.ones(batch.size(0), 1).to(device)
            fake_labels = torch.zeros(batch.size(0), 1).to(device)

            # Treinar discriminador
            optimizer_d.zero_grad()
            outputs_real = discriminator(batch)
            d_loss_real = criterion_d(outputs_real, real_labels)

            z = torch.randn(batch.size(0), args['n_z']).to(device)
            fake_data = decoder(z)
            outputs_fake = discriminator(fake_data.detach())
            d_loss_fake = criterion_d(outputs_fake, fake_labels)

            d_loss = d_loss_real + d_loss_fake
            d_loss.backward()
            optimizer_d.step()

            # Treinar gerador
            optimizer_g.zero_grad()
            outputs = discriminator(fake_data)
            g_loss = criterion_g(fake_data, batch) + criterion_d(outputs, real_labels)
            g_loss.backward()
            optimizer_g.step()

    return encoder, decoder, discriminator

def process_data(input_file, output_file):
    """
    Processa os dados, gera amostras sintéticas e salva o dataset balanceado.

    Args:
        input_file: Caminho do arquivo .csv de entrada.
        output_file: Caminho do arquivo .csv de saída.
    """
    try:
        # Carregar dados
        data = pd.read_csv(input_file)
    except Exception as e:
        print(f"Erro ao ler o arquivo {input_file}: {e}")
        return

    # Separar features e rótulos (última coluna é a classe)
    X = data.iloc[:, :-1].values  # Todas as colunas, exceto a última
    y = data.iloc[:, -1].values   # Última coluna é a classe

    print(f"Porcentagem Distribuição das classes (%):\n{pd.Series(y).value_counts(normalize=True) * 100}\n")

    # Inicializar modelos GAN
    num_features = X.shape[1]
    encoder = Encoder(args, num_features).to(device)
    decoder = Decoder(args, num_features).to(device)
    discriminator = Discriminator(num_features).to(device)

    # Treinar GAN
    encoder, decoder, _ = train_gan(encoder, decoder, discriminator, X, args)

    # Gerar amostras sintéticas
    n_to_sample_dict, _ = calculate_n_to_sample(y)
    synthetic_data, synthetic_labels = [], []

    for cl, n_samples in n_to_sample_dict.items():
        if n_samples > 0:
            X_synthetic, y_synthetic = G_SM1(X, y, n_samples, cl, encoder, decoder, args)
            synthetic_data.append(X_synthetic)
            synthetic_labels.append(y_synthetic)

    if synthetic_data:
        X_synthetic_combined = np.vstack(synthetic_data)
        y_synthetic_combined = np.hstack(synthetic_labels)
        X_combined = np.vstack([X, X_synthetic_combined])
        y_combined = np.hstack([y, y_synthetic_combined])
    else:
        X_combined = X
        y_combined = y

    # Mostrar distribuição das classes após o balanceamento
    print(f"Porcentagem Distribuição das classes após o balanceamento (%):\n{pd.Series(y_combined).value_counts(normalize=True) * 100}\n")

    # Salvar dataset balanceado
    balanced_data = pd.DataFrame(X_combined, columns=data.columns[:-1])
    balanced_data['class'] = y_combined  # Adiciona a coluna de classes
    balanced_data.to_csv(output_file, index=False)
    print(f"Dataset balanceado salvo em: {output_file}")

# Interação com o usuário
if __name__ == "__main__":
    print("Bem-vindo ao gerador de datasets balanceados!")
    input_file = input("Digite o caminho do arquivo .csv de entrada: ")
    output_file = input("Digite o caminho do arquivo .csv de saída: ")

    process_data(input_file, output_file)
    print("Processo concluído!")