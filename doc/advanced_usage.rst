Advanced usage
==============

In this section we provide some examples of more advanced usages of the library.

Building dynamic systems
------------------------

The ``QPU`` interface provides a method called ``evaluate``. This method builds the quantum circuit corresponding to a given QRBS, in order to see if the QPU used can run the given system. While this method is mainly intended to be used inside the ``execute``, it can also be used to build dynamic systems.

For example, let's build a QRBS by concatenating rules one after the other:

1. IF *X0* THEN *X1*
2. IF *X1* THEN *X2*

Up until:

N. IF *X(N-1)* then *XN*

It is possible that such a system cannot be executed in a given ``QPU`` if it surpases the amount of qubits available. Therefore, to build a system like this but satisfying the limits of the ``QPU`` we can do something like the following:

.. code::

    system = QRBS()
    facts = []
    rules = []
    island = None

    for i in range(1,n):
        facts.append(system.assert_fact('{}'.format(i), 'Fact {}'.format(i), 1.0))
        if len(facts) == 1: # add both facts in the case of the first rule
            facts.append(system.assert_fact('{}'.format(i-1), 'Fact {}'.format(i-1), 1.0))
        rules.append(system.assert_rule(facts[-2], facts[-1], 1.0)) # use the last facts to make a rule
        island = system.assert_island(rules)
        try:
            MyQlmQPU.evaluate(system)
            if i != n - 1:
                system.retract_island(island) # remove the island once it has been checked, a new one will be added in the next loop
        except ValueError:
            system.retract_island(island)
            system.retract_rule(rules.pop(-1))
            system.retract_fact(facts.pop(-1))
            island = system.assert_island(rules)

In this example, we add the rules one by one and check the evaluation result with each addition. When the knowledge island composed by the rules is too large for ``MyQlmQPU`` to execute it, we retract the last rule of the set (we do the same with the last fact) and assert the previous ones.

Comparing models
----------------

``MyQlmQPU`` offers three different models to implement the quantum circuit of a given QRBS. These models, based on classical models of rule based systems, are:

* Certainty factors (``cf``)
* Fuzzy logic (``fuzzy``)
* Bayesian networks (``bayes``)

The certainty factors model is used by default, to use any of the other one simply indicate it in the methods ``evaluate`` and ``execute``:

.. code::

    MyQlmQPU.execute(system, model='fuzzy')

While at their core all models work the same (relate precedent with consequents through rules), it can be interesting to compare the results obtained with each of them:

.. code::

    models = ['cf', 'fuzzy', 'bayes']
    results = []

    for model in models:
        MyQlmQPU.execute(system, model=model)
        results.append(consequent.precision)

    print(zip(models, results)) # [('cf', 0.978), ('fuzzy', 0.963), ('bayes', 0.989)]

