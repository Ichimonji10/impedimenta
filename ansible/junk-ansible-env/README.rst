junk-ansible-env
================

Demonstrate how ansible-env differs depending on whether it's executed in ad-hoc
mode or playbook mode. To demonstrate, compare the output of these commands:

.. code-block:: sh

    for var in ansible_env ansible_facts; do
        ansible all \
            -i localhost, \
            -m debug \
            -a "var=${var}"
    done

To the output of the following:

.. code-block:: sh

    ansible-playbook site.yml -i localhost,
