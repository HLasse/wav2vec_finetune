for CONFIG in configs/wav2vec_configs/*.json; do python train_wav2vec.py $CONFIG; done