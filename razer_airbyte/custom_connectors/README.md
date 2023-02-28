
1. build connector image from the connector source/destination directory:

    ```shell
    docker build -t source_yahoo_example:latest .
    ```

2. start docker registry

    ```shell
    docker run -d -p 5000:5000 --restart=always --name registry registry:2.7
    docker run -d -p 5005:5000 --name registry registry:2.7
    ```


3. tag the image

    ```shell
    docker tag source_yahoo_example:latest localhost:5005/source_yahoo_example:latest
    ```

4. push connector image to the registry

    ```shell
    docker push localhost:5005/source_yahoo_example:latest
    ```

