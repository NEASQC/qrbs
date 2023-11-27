Basic usage
===========

In this section we provide some examples of how to use the basic functions of this library. Each of the examples continues where the prior one left, so we recommend to read this page in order for the first time.

Your first QRBS
---------------

We begin these examples by creating and populating a QRBS. We use the inferential circuit below as the structure for our system. This ciricuit is made from the following rules:

1. IF *A* AND *B* THEN *X*
2. IF *X* OR *C* THEN *Y*
3. IF (*D* OR *E*) AND *Y* THEN *R*

.. image::  img/inferential_circuit.svg
    :width: 400
    :alt: Inferential circuit

We recommend using the following approach to build any QRBS:

1. Assert all the facts from the left hand side of the rules.
2. Assert all the facts from the right hand side of the rules.
3. Assert all the rules that relate the facts.
4. Assert the knowledge islands with their corresponding rules.

In this case, we can obtain the corresponding QRBS with the code below:

.. code::
    
    system = QRBS()

    a = system.assert_fact('A', 'Fact A')
    b = system.assert_fact('B', 'Fact B')
    c = system.assert_fact('C', 'Fact C')
    d = system.assert_fact('D', 'Fact D')
    e = system.assert_fact('E', 'Fact E')
    
    x = system.assert_fact('X', 'Fact X')
    y = system.assert_fact('Y', 'Fact Y')
    r = system.assert_fact('R', 'Fact R')

    rule_1 = system.assert_rule(AndOperator(a,b), x)
    rule_2 = system.assert_rule(OrOperator(x,c), y)
    rule_3 = system.assert_rule(AndOperator(OrOperator(d,e),y), r)

    island = system.assert_island([rule_1, rule_2, rule_3])

With this code, we have the QRBS corresponding to the initial inferential circuit encoded into the variable ``system``. 

During the process of asserting elements you may run into some errors, all of which include a message explaining what went wrong.


Managing uncertainty
--------------------

Once we have declared a QRBS and have it populated with declarative and procedural knowledge, we can manage the uncertain knowledge through the precision of facts and the certainty or rules. For example, let's say we want all of our facts to be equally true and false. Therefore

.. code::

    for fact in [a,b,c,d,e]:
        fact.precision = 0.5

Notice how we only modify the precision value for the facts that are part of a left hand side of a rule, since the facts that belong to the right hand sides will have their precision calculated when executing the system.

We can follow the same approach for the rules. In this case, we want to give them different values of certainty to each of them.

.. code::

    rule_1.certainty = 0.1618
    rule_2.certainty = 0.42
    rule_3.certainty = 0.3141592

By managing uncertainty like this, the system already keeps track of them.


Executing the system
--------------------

To execute a populated QRBS, we simply call the ``execute`` method of any of the available implementations of the class ``QPU``. We provide the ``MyQlmQPU`` implementation, and to use it we would do as follows:

.. code::

    MyQlmQPU.execute(system)

Once the system has been executed, we can check the precision values of the right hand sides to see how they have changed, according to the rules of the system. For example:

.. code::

    system = QRBS()

    precedent = system.assert_fact('p', 'Precedent')
    precedent.precision = 1.0
    consequent = system.assert_fact('c', 'Consequent')
    
    print(consequent.precision) # 0.0

    rule = system.assert_rule(precedent, consequent)
    rule.certainty = 1.0
    island = system.assert_island([rule])

    MyQlmQPU.execute(system)

    print(consequent.precision) # 1.0
    
