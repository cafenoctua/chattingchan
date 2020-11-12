# 環境構築
## モデル環境構築
GPU環境で開発するのにDockerを使う
以下のコマンドがGPUをマウントしつつjupyter Notebookのポートとつなぐ
```--gpus all```で全GPUにつなぎに行く
```
docker run --gpus all -v ${PWD}/Notebooks:/work -p {host port}:{Docker port} {image tag}
```