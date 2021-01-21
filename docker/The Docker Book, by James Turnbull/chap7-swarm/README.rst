chap7-swarm
===========

Start larry, curly, and moe. On larry, start the swarm leader, and get information about the host as
desired:

.. code:: bash

    ./start-leader.sh
    docker swarm join-token worker  # in case output from above is lost
    docker node ls

The swarm leader will print a command with which workers can join. Execute that command on curly and
moe. Even if hosts reboot, the swarm will eventually re-converge. Once workers are present, start a
service from the leader:

.. code:: bash

    ./start-replicated-service.sh
    docker service ls
    docker service inspect --pretty replicated_heyworld
    docker service ps replicated_heyworld
    docker service scale replicated_heyworld=3
    docker service rm replicated_heyworld

The above can also be done with a global service, with the difference that the ``docker service
scale ...`` command won't work.
