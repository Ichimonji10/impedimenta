Chapter 9
=========


.. code:: bash

    # spin up a deployment and a service, and verify they're up
    kubectl apply \
        --filename=../chap6/svc-lke.yml \
        --filename=../chap7/deploy.yml
    kubectl get deployment
    kubectl get svc
    xdg-open "http://$(
        kubectl get svc cloud-lb --output=jsonpath='{.status.loadBalancer.ingress[0].hostname}'
    )"

    # apply a rolling update
    kubectl apply --filename=deploy.yml
    kubectl get deployments
    kubectl get pods
    kubectl rollout status deployment qsk-deploy

    # clean up
    kubectl delete services,deployments,pods --all
