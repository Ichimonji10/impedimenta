Chapter 12
==========

To see which IP addresses are bound to a container:

.. code:: sh

    docker container inspect \
        --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' \
        $(docker container ls --quiet)

To see which IP addresses have been bound to containers within the context of an overlay network:

.. code:: sh

    docker network inspect uber-net \
        --format '{{ range .Containers }}{{ .IPv4Address }}{{ "\n" }}{{ end}}'
