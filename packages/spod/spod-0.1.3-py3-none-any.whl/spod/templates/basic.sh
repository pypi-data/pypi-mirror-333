#!/bin/bash

#SBATCH --job-name=<JOB_NAME>
#SBATCH -D .
#SBATCH --output=O-%x.%j
#SBATCH --error=E-%x.%j
#SBATCH --nodes=8                   # number of nodes
#SBATCH --ntasks-per-node=1         # number of MP tasks
#SBATCH --gpus-per-task=8
#SBATCH --cpus-per-task=80         # number of cores per tasks
#SBATCH --mem=60G
#SBATCH --time=72:00:00             # maximum execution time (HH:MM:SS)

######################
### Set enviroment ###
######################
source activate pytorch
source /usr/share/modules/init/bash 
module load cuda/12.1 nccl/2.18.3-cuda.12.1 nccl_efa/1.24.1-nccl.2.18.3-cuda.12.1 
export HF_DATASETS_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
export GPUS_PER_NODE=8

######################

######################
#### Set network #####
######################
head_node_ip=$(scontrol show hostnames $SLURM_JOB_NODELIST | head -n 1)
NODE_RANK=$SLURM_PROCID
######################

export LAUNCHER="accelerate launch \
    --num_processes $((SLURM_NNODES * GPUS_PER_NODE)) \
    --num_machines $SLURM_NNODES \
    --rdzv_backend c10d \
    --mixed_precision fp16 \
    --main_process_ip $head_node_ip \
    --main_process_port 29500 \
    "

export SCRIPT="/home/normanm/code/LUI/train_lui.py"
export SCRIPT_ARGS=" \
    conf/lui/s_lui_dec_1k_p8_con0_proxy.yaml \
    "
# This step is necessary because accelerate launch does not handle multiline arguments properly
export CMD="$LAUNCHER $SCRIPT $SCRIPT_ARGS" 
srun $CMD