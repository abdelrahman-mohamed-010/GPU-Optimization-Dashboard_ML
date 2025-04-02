import torch
import torch.nn as nn

cuda_available=torch.cuda.is_available()
print(f"CUDA Available: {cuda_available}")


class NNPredictor(nn.Module):
    def __init__(self, input_dim=2,hidden_dim=128, output_dim=1):
        super(NNPredictor,self).__init__()
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

_predicctor = None

def load_predictor(model_path="ai_model/nnp_model.pth"):
    global _predictor
    if _predictor is None:
        _predictor = NNPredictor()
        _predictor.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
        _predictor.eval()
    return _predictor

def predict_best_gpu(task, gpu_features):
    model = load_predictor()
    best_score = float('inf')
    best_gpu = None
    for gpu_id, features in gpu_features.items():
        x = torch.tensor(features, dtype=torch.float32).unsqueeze(0)
        score = model(x).item()
        if score < best_score:
            best_score = score
            best_gpu = gpu_id
    return best_gpu