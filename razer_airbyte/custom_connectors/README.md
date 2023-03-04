
1. build connector image from the connector source/destination directory:

    ```shell
    docker build -t my-image-name:latest .
    ```

2. start docker registry

    ```shell
    docker run -d -p 5005:5000 --name registry registry:2.7
    ```


3. tag the image

    ```shell
    docker tag my-image-name:latest localhost:5005/my-image-name:latest
    ```

4. push connector image to the registry

    ```shell
    docker push localhost:5005/my-image-name:latest
    ```

