Chapter 4 with Linode
=====================

After provisioning a k8s cluster with Linode, download the kubeconfig file from the Linode k8s
cluster page, and verify kubectl can contact the cluster:

.. code:: bash

    # Explicitly reference kubeconfig
    kubectl --kubeconfig ~/Downloads/jaudet-kubeconfig.yaml get nodes

    # Implicitly reference kubeconfig
    install -Dm600 ~/Downloads/jaudet/kubeconfig.yaml ~/.kube/config
    kubectl get nodes
