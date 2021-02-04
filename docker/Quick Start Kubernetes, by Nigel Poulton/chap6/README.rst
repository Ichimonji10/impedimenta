Chapter 6
=========

.. code:: bash

    # post pod definition to k8s, and learn about pod
    kubectl apply --filename=pod.yml
    kubectl get pods
    kubectl describe pod first-pod

    # post service definition to k8s, and learn about service
    kubectl apply --filename=svc-lke.yml
    kubectl get svc
    kubectl describe svc cloud-lb
    xdg-open "http://$(kubectl get svc cloud-lb --output=jsonpath='{.spec.clusterIP}')"

    # clean up
    kubectl delete svc cloud-lb
    kubectl delete pod first-pod
