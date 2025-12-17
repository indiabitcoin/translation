# AWS GPU Requirements for Translation Models

## Quick Answer

For **NLLB-200-3.3B** (recommended model):
- **Minimum**: AWS `g4dn.xlarge` (1x NVIDIA T4, 16GB VRAM)
- **Recommended**: AWS `g4dn.2xlarge` (1x NVIDIA T4, 16GB VRAM, more CPU/RAM)
- **Optimal**: AWS `g5.xlarge` (1x NVIDIA A10G, 24GB VRAM)

## GPU Requirements by Model

### NLLB-200 Models

| Model Size | Parameters | VRAM Needed | AWS Instance | Cost/Hour (approx) |
|------------|------------|-------------|--------------|-------------------|
| **600M** | 600M | 2-4GB | `g4dn.xlarge` | $0.526 |
| **1.3B** | 1.3B | 4-6GB | `g4dn.xlarge` | $0.526 |
| **3.3B** ⭐ | 3.3B | 8-12GB | `g4dn.2xlarge` | $0.752 |
| **54.5B** | 54.5B | 40GB+ | `g5.12xlarge` | $5.67 |

### M2M-100 Models

| Model Size | Parameters | VRAM Needed | AWS Instance | Cost/Hour (approx) |
|------------|------------|-------------|--------------|-------------------|
| **418M** | 418M | 2-4GB | `g4dn.xlarge` | $0.526 |
| **1.2B** | 1.2B | 4-6GB | `g4dn.xlarge` | $0.526 |
| **12B** | 12B | 24GB+ | `g5.2xlarge` | $1.408 |

## Recommended AWS GPU Instances

### For NLLB-200-3.3B (Recommended)

#### Option 1: g4dn.2xlarge ⭐ BEST VALUE
```
Instance: g4dn.2xlarge
GPU: 1x NVIDIA T4 (16GB VRAM)
vCPU: 8
RAM: 32GB
Network: Up to 25 Gbps
Cost: ~$0.752/hour (~$540/month)
```

**Why this is best:**
- ✅ Sufficient VRAM for 3.3B model
- ✅ Good CPU/RAM for preprocessing
- ✅ Cost-effective
- ✅ Good for production workloads

#### Option 2: g5.xlarge (Better Performance)
```
Instance: g5.xlarge
GPU: 1x NVIDIA A10G (24GB VRAM)
vCPU: 4
RAM: 16GB
Network: Up to 25 Gbps
Cost: ~$1.408/hour (~$1,014/month)
```

**Why choose this:**
- ✅ More VRAM headroom
- ✅ Faster GPU (A10G vs T4)
- ✅ Better for high-traffic scenarios

#### Option 3: g4dn.xlarge (Budget Option)
```
Instance: g4dn.xlarge
GPU: 1x NVIDIA T4 (16GB VRAM)
vCPU: 4
RAM: 16GB
Network: Up to 25 Gbps
Cost: ~$0.526/hour (~$379/month)
```

**Why choose this:**
- ✅ Lowest cost with GPU
- ✅ Sufficient for 3.3B model (with optimization)
- ⚠️ May need model quantization for best performance

### For Larger Models (NLLB-200-54.5B or M2M-100-12B)

#### Option: g5.12xlarge
```
Instance: g5.12xlarge
GPU: 4x NVIDIA A10G (24GB VRAM each = 96GB total)
vCPU: 48
RAM: 192GB
Network: Up to 50 Gbps
Cost: ~$5.67/hour (~$4,082/month)
```

**When needed:**
- Very large models (54.5B parameters)
- Maximum quality requirements
- High-volume production

## AWS Instance Comparison

### g4dn Series (NVIDIA T4)

| Instance | GPU | VRAM | vCPU | RAM | Cost/Hour |
|----------|-----|------|------|-----|-----------|
| g4dn.xlarge | 1x T4 | 16GB | 4 | 16GB | $0.526 |
| g4dn.2xlarge | 1x T4 | 16GB | 8 | 32GB | $0.752 |
| g4dn.4xlarge | 1x T4 | 16GB | 16 | 64GB | $1.204 |

**Best for:** NLLB-200-3.3B, cost-effective production

### g5 Series (NVIDIA A10G)

| Instance | GPU | VRAM | vCPU | RAM | Cost/Hour |
|----------|-----|------|------|-----|-----------|
| g5.xlarge | 1x A10G | 24GB | 4 | 16GB | $1.408 |
| g5.2xlarge | 1x A10G | 24GB | 8 | 32GB | $1.516 |
| g5.4xlarge | 1x A10G | 24GB | 16 | 64GB | $1.732 |
| g5.12xlarge | 4x A10G | 96GB | 48 | 192GB | $5.67 |

**Best for:** Larger models, higher performance needs

### p3 Series (NVIDIA V100) - Older but Powerful

| Instance | GPU | VRAM | vCPU | RAM | Cost/Hour |
|----------|-----|------|------|-----|-----------|
| p3.2xlarge | 1x V100 | 16GB | 8 | 61GB | $3.06 |
| p3.8xlarge | 4x V100 | 64GB | 32 | 244GB | $12.24 |

**Note:** More expensive, older architecture, but still powerful

## Cost Optimization Strategies

### 1. Use Spot Instances (Save 70-90%)

```bash
# Spot instance pricing (example)
g4dn.2xlarge: $0.752/hour → ~$0.15-0.22/hour (spot)
Savings: 70-90% discount
```

**Trade-offs:**
- ⚠️ Can be interrupted (2-minute warning)
- ✅ Great for development/testing
- ✅ Can work for production with proper handling

### 2. Model Quantization (Reduce VRAM)

```python
# Use 8-bit quantization
from transformers import BitsAndBytesConfig

quantization_config = BitsAndBytesConfig(
    load_in_8bit=True,
    llm_int8_threshold=6.0
)

model = AutoModelForSeq2SeqLM.from_pretrained(
    "facebook/nllb-200-3.3B",
    quantization_config=quantization_config
)
```

**Benefits:**
- ✅ 50% VRAM reduction
- ✅ Can use smaller GPU instances
- ✅ Minimal quality loss

### 3. Use CPU-Only (No GPU) - For Smaller Models

For **NLLB-200-600M** or **Argos Translate**:
- **Instance**: `c6i.2xlarge` or `m6i.2xlarge`
- **Cost**: ~$0.34/hour (~$245/month)
- **Performance**: Slower but much cheaper

### 4. Hybrid Approach

- **GPU instance**: For NLLB direct translations
- **CPU instance**: For Argos Translate (lightweight)
- **Load balancer**: Route requests appropriately

## Deployment Architecture

### Recommended Setup

```
┌─────────────────┐
│  Application    │
│  Load Balancer  │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼───┐ ┌──▼────┐
│ GPU   │ │ CPU   │
│ NLLB  │ │ Argos │
│ g4dn  │ │ c6i   │
└───────┘ └───────┘
```

**Cost breakdown:**
- GPU instance (g4dn.2xlarge): $0.752/hour
- CPU instance (c6i.2xlarge): $0.34/hour
- **Total**: ~$1.09/hour (~$785/month)

## Specific Recommendations

### For Your Use Case (Translation API)

**Recommended: g4dn.2xlarge**

**Why:**
1. ✅ Handles NLLB-200-3.3B comfortably
2. ✅ Good balance of cost and performance
3. ✅ Sufficient for production traffic
4. ✅ Can handle multiple concurrent requests

**Configuration:**
```yaml
Instance Type: g4dn.2xlarge
GPU: 1x NVIDIA T4 (16GB)
vCPU: 8
RAM: 32GB
Storage: 100GB GP3 SSD
Cost: ~$0.752/hour (~$540/month)
```

### If Budget is Tight

**Option: g4dn.xlarge with quantization**
- Use 8-bit quantization
- Cost: ~$0.526/hour (~$379/month)
- Still good performance

### If You Need Maximum Performance

**Option: g5.xlarge**
- Better GPU (A10G)
- More VRAM headroom
- Cost: ~$1.408/hour (~$1,014/month)

## Setup Instructions

### Step 1: Launch EC2 Instance

```bash
# Using AWS CLI
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type g4dn.2xlarge \
  --key-name your-key-pair \
  --security-group-ids sg-xxxxxxxxx \
  --subnet-id subnet-xxxxxxxxx \
  --block-device-mappings '[{"DeviceName":"/dev/sda1","Ebs":{"VolumeSize":100,"VolumeType":"gp3"}}]'
```

### Step 2: Install CUDA and Dependencies

```bash
# Connect to instance
ssh -i your-key.pem ec2-user@your-instance-ip

# Install NVIDIA drivers (if not pre-installed)
sudo yum install -y kernel-devel-$(uname -r) kernel-headers-$(uname -r)
wget https://developer.download.nvidia.com/compute/cuda/repos/rhel7/x86_64/cuda-repo-rhel7-11.8.0-520.61.05-1.x86_64.rpm
sudo rpm -i cuda-repo-rhel7-11.8.0-520.61.05-1.x86_64.rpm
sudo yum clean all
sudo yum -y install cuda

# Install Python and PyTorch with CUDA
python3 -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
python3 -m pip install transformers accelerate sentencepiece
```

### Step 3: Deploy Your Application

```bash
# Clone your repository
git clone https://github.com/indiabitcoin/translation.git
cd translation

# Install dependencies
pip install -r requirements.txt

# Run with GPU
python main.py
```

## Cost Estimates

### Monthly Costs (24/7 operation)

| Instance | Hourly | Monthly | Use Case |
|----------|--------|---------|----------|
| g4dn.xlarge | $0.526 | ~$379 | Budget option |
| g4dn.2xlarge | $0.752 | ~$540 | **Recommended** |
| g5.xlarge | $1.408 | ~$1,014 | High performance |
| g5.12xlarge | $5.67 | ~$4,082 | Large models |

### With Spot Instances (70% savings)

| Instance | Hourly (Spot) | Monthly | Savings |
|----------|---------------|---------|---------|
| g4dn.2xlarge | ~$0.22 | ~$162 | 70% off |

## Monitoring and Optimization

### Check GPU Usage

```bash
# Install nvidia-smi
nvidia-smi

# Monitor continuously
watch -n 1 nvidia-smi
```

### Optimize Batch Processing

```python
# Process multiple translations in batch
def translate_batch(texts, source, target, batch_size=8):
    # Process in batches to maximize GPU utilization
    results = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        batch_results = model.translate_batch(batch, source, target)
        results.extend(batch_results)
    return results
```

## Summary

**For NLLB-200-3.3B deployment:**

✅ **Recommended**: `g4dn.2xlarge`
- Cost: ~$540/month
- Performance: Excellent
- VRAM: Sufficient (16GB)

✅ **Budget Option**: `g4dn.xlarge` with quantization
- Cost: ~$379/month
- Performance: Good
- VRAM: Sufficient with 8-bit quantization

✅ **High Performance**: `g5.xlarge`
- Cost: ~$1,014/month
- Performance: Excellent
- VRAM: More headroom (24GB)

---

**Bottom Line**: Start with **g4dn.2xlarge** - it's the sweet spot for cost and performance for NLLB-200-3.3B model.

