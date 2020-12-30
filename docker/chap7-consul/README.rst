chap7-consul
============

.. NOTE:: This project doesn't work because it attempts to bind containers to port 53.

Pick a host to be the bootstrap host. I'm arbitrarily picking larry. Start the bootstrap consul
server on larry:

.. code:: bash

    ./create-leader-env.sh
    docker-compose --env-file .leader.env up

On curly and moe, set larry's IP address and start consul:

.. code:: bash

    ./create-follower-env.sh
    docker-compose --env-file .follower.env up
