
1. build connector image from the connector source/destination directory:

    ```shell 
    docker build -t my-image-name:latest .
    ```

2. tag the image

    ```shell 
   docker tag local-image:tagname new-repo:tagname
    ```

3. push connector image to the registry

    ```shell
       docker push new-repo:tagname
    ```

