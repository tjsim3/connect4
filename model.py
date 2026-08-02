import torch
from tqdm import tqdm

from generatedata import generateStageOne


def save_model(model, filename):
    torch.save(model.state_dict(), filename)


def load_model(filename):
    model = NeuralNetwork()
    model.load_state_dict(torch.load(filename))
    model.eval()
    return model

class NeuralNetwork(torch.nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        self.flatten = torch.nn.Flatten()
        self.linear_relu_stack = torch.nn.Sequential(
            torch.nn.Linear(43, 128),
            torch.nn.ReLU(),
            torch.nn.Linear(128, 64),
            torch.nn.ReLU(),
            torch.nn.Linear(64, 7)
        )

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits


def trainStageOne(samples, epochs, d=False):
    print("I made it to the training function")
    model = NeuralNetwork()
    loss_fn = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    if not d:
        data, labels, players = generateStageOne(samples)
    else:
        data, labels, players = generateStageOne(samples, d=True)

    
    for i in range(len(data)):
        flat = []

        for row in data[i]:
            flat.extend(row)
        flat.append(players[i])
        data[i] = flat
        
    data = torch.tensor(data, dtype=torch.float32)
    labels = torch.tensor(labels, dtype=torch.long)
    print("I finished making tensors")

    for epoch in tqdm(range(epochs)):
        model.train()
        optimizer.zero_grad()
        output = model(data)
        loss = loss_fn(output, labels)
        loss.backward()
        optimizer.step()


    print("I finished training")
    print(f"Final loss: {loss.item()}") if not UnboundLocalError else print("Loss unbound")
    return model