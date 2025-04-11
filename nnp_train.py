import time
import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import os

cuda_available=torch.cuda.is_available()
print(f"CUDA Available: {cuda_available}")


class NNP(nn.Module):
    def __init__(self, input_dim=2,hidden_dim=128, output_dim=1):
        super(NNP,self).__init__()
        self.model = nn.Sequential(
            nn.Linear(input_dim,hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim,hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim,hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim,output_dim)
        )
    
    def forward(self,x):
        return self.model(x)
    

def train_model(model,data_loader, epochs=10,lr=0.001):
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(),lr=lr)
    model.train()
    for epoch in range(epochs):
        epoch_loss = 0.0
        for inputs, targets in data_loader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()
            epoch_loss+=loss.item()
        print(f"Epoch {epoch+1}/{epochs}, Loss: {epoch_loss/len(data_loader): .4f}")
    return model

def falback_heuristic(gpu_states):
    gpu_states_sorted= sorted(gpu_states,key=lambda x: x[1])
    return gpu_states_sorted[0][0]

def r2_score(y_true, y_pred):
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return 1 - (ss_res / ss_tot)


def test_inference(model, X_test, y_test):
    model.eval()
    num_samples = X_test.shape[0]
    total_time = 0.0
    predictions = []
    with torch.no_grad():
        for i in range(num_samples):
            input_sample=X_test[i].unsqueeze(0)
            start = time.time()
            pred = model(input_sample)
            total_time += (time.time()-start)
            predictions.append(pred.item())
    avg_inference_time_ms = (total_time/num_samples)*1000
    predictions = np.array(predictions)
    ground_truth = y_test.numpy().flatten()
    mae =np.mean(np.abs(predictions-ground_truth))
    r2 = r2_score(ground_truth, predictions)

    print(f"Tested {num_samples} samples.")
    print(f"Average inference time: {avg_inference_time_ms:.2f} ms per task.")
    print(f"Mean Absolute Error (MAE): {mae:.2f}")
    print(f"R^2 Score: {r2:.2f}")
    return avg_inference_time_ms, mae, r2

def main():
    MODEL_PATH = "ai_model/nnp_model.pth"
    df_train = pd.read_csv("data/simulation/task_gpu_pairs.csv")
    # df_train = df.sample(n=500000, random_state=42)

    X = df_train[["utilization","memory_used_gb"]].values
    y = (100-df_train["utilization"]).values.reshape(-1,1)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.10, random_state=42
    )
    
    # Convert data to PyTorch tensors
    X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
    y_train_tensor = torch.tensor(y_train, dtype=torch.float32)
    X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
    y_test_tensor = torch.tensor(y_test, dtype=torch.float32)
    
    # Create DataLoader for training
    train_dataset = torch.utils.data.TensorDataset(X_train_tensor, y_train_tensor)
    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=64, shuffle=True)

    if os.path.exists(MODEL_PATH):
        print("Loadking existing model......")
        model = torch.load(MODEL_PATH,weights_only=False)
    else:
        os.makedirs("ai_model",exist_ok=True)
        model= NNP()
        print("Training the NNP model.....")
        model = train_model(model,train_loader,epochs=50,lr=0.001)

        torch.save(model,MODEL_PATH)
        print(f"Model saved to {MODEL_PATH}")

    print("\nTesting inference speed and accuracy on the test set...")
    avg_time, mae, r2 = test_inference(model, X_test_tensor, y_test_tensor)

    sample_imput=torch.tensor([[20.0,80.0]],dtype=torch.float32)
    model.eval()
    start_time = time.time()
    with torch.no_grad():
        prediction = model(sample_imput)
    inference_time = (time.time()-start_time)*1000
    print(f"Inference time: {inference_time:.2f} ms, Predicted suitability: {prediction.item():.2f}")

    prediction_value= prediction.item()
    if prediction_value<80:
        print("Low-confidence prediction(<80). Applying falback heuristic.")
        simulated_gpu_states=[
            ("GPU_1",30),
            ("GPU_2",45),
            ("GPU_3",25),
            ("GPU_4",50)
        ]
        selected_gpu = falback_heuristic(simulated_gpu_states)
        print(f"Fallback selected GPU: {selected_gpu}")
    else:
        print("NNP prediction is confident. Use the predicted GPU assignment.")

if __name__=="__main__":
    main()