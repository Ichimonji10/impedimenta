Chapter 7
=========

.. code:: bash

    # post deployment definition to k8s, and learn about it
    kubectl apply --filename=deploy.yml
    kubectl get deployments qsk-deploy
    kubectl get pods

    # delete pod, and watch recovery
    kubectl delete pod "$(kubectl get pods --output=jsonpath='{.items[0].metadata.name}')"
    kubectl get deployments qsk-deploy
    kubectl get pods

    # See nodes, and on which node each pod is running. Do this before and after deleting a node
    # from the Linode web interface. Linode will eventually replace the deleted node, as a feature
    # of LKE.
    kubectl get nodes
    kubectl get pods --output=wide
