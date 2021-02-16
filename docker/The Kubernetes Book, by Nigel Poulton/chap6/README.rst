Chapter 6
=========

Within a ``Service`` manifest, ``.spec.type`` may be one of the following:

``ClusterIP``
    The default. It provides a stable IP address internally within the cluster.

``NodePort``
    Builds on top of ``ClusterIP`` and makes a port accessible from outside the cluster.

``LoadBalancer``
    Builds on top of ``NodePort`` and integrates with a cloud-based load-balancer.

``ExternalName``
    Directs traffic to services that exist outside of the cluster.

Depending on what type of service you've deployed, and how you've deployed it, the method for
accessing the service varies. If using a ``LoadBalancer`` and Linode Kubernetes Engine, the
following will work:

.. code:: bash

    xdg-open http://$(
        kubectl get svc "${svc_name}" --output=jsonpath='{.status.loadBalancer.ingress[0].hostname}'
    )

If using ``NodePort`` and minikube:

.. code:: bash

    minikube service "${svc_name}"

Theoretically, you could also access the ``NodePort`` on any node, but this will only work if nodes
have sufficiently lax firewall rules.
