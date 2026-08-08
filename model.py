import torch
from torch.utils.data import DataLoader, TensorDataset
from tqdm import tqdm

from generatedata import generateStageOne


def save_model(model, filename):
    torch.save(model.state_dict(), filename)


def load_model(filename):
    model = NeuralNetwork()
    model.load_state_dict(torch.load(filename))
    model.eval()
    return model

def loadData(path, batch_size=64):
    saved = torch.load(path)
    data = saved["data"]
    labels = saved["labels"]
    players = saved["players"]

    dataset = TensorDataset(data, labels, players)

    loader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=True
    )

    return loader

def trainStageOne(samples, epochs, d="False"):
    print("I made it to the training function")
    if epochs <= 0:
        raise ValueError("epochs must be greater than 0")
    
    model = NeuralNetwork()
    loss_fn = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    loader = loadData("datasets/stage1_data_10k.pt", batch_size=64)

    for epoch in tqdm(range(epochs)):
        model.train()
        for data, labels, player in loader:
            data = data.view(data.size(0), -1)
            data = torch.cat(
                (data, player.unsqueeze(1).float()),
                dim=1
            )

            optimizer.zero_grad()
            output = model(data)
            loss = loss_fn(output, labels)
            loss.backward()
            optimizer.step()
            
    print("I finished training")
    return model

class NeuralNetwork(torch.nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        self.flatten = torch.nn.Flatten()
        self.linear_relu_stack = torch.nn.Sequential(
            torch.nn.Linear(43, 17),
            torch.nn.ReLU(),
            torch.nn.Linear(17, 16),
            torch.nn.ReLU(),
            torch.nn.Linear(16, 7)
        )

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits