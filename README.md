# 環境構築
## モデル環境構築
GPU環境で開発するのにDockerを使う
以下のコマンドがGPUをマウントしつつjupyter Notebookのポートとつなぐ
```--gpus all```で全GPUにつなぎに行く
```
docker run --gpus all -v ${PWD}/Notebooks:/work -p {host port}:{Docker port} {image tag}
```

# Memos
デタッチドモードでコンテナ起動
```
docker run --name ubuntu_bash -d -it {Container ID} bash
```
起動中のコンテナのCLIに入る
```
docker exec -it ubuntu_bash2 bash
```