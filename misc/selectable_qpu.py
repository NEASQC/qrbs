import sys
from abc import ABC, abstractmethod
from qat.lang.AQASM import Program
sys.path.append("../")
from neasqc_qrbs.knowledge_rep import BuilderImpl, BuilderFuzzy, BuilderBayes

class QPU(ABC): # pragma: no cover
    """Interface defining the structure to implement Quantum Processing Units (QPU).
    """
        
    @staticmethod
    @abstractmethod
    def evaluate(qrbs) -> bool:
        """Evaluates whether a QRBS can be executed on this QPU.

        Args:
            qrbs (:obj:`QRBS`): The QRBS to be evaluated.
        """
        pass

    @staticmethod
    @abstractmethod
    def execute(qrbs) -> None:
        """Executes the QRBS on this QPU.

        Args:
            qrbs (:obj:`QRBS`): The QRBS to be executed.
        """
        pass

class SelectableQPU(QPU):
    """Implementation of a backend-selectable QPU.
    """
    
    MAX_ARITY = 34
    BUILDERS = {
        'cf': BuilderImpl,
        'fuzzy': BuilderFuzzy,
        'bayes': BuilderBayes
    }

    @staticmethod
    def evaluate(qrbs, eval_islands=None, model='cf', qpu='python') -> bool:
        """Evaluates whether a QRBS can be executed on this QPU.

        Args:
            qrbs (:obj:`QRBS`): The QRBS to be evaluated.
            eval_islands (List[:obj:`~neasqc_qrbs.knowledge_rep.KnowledgeIsland`], optional): A list of specific KnowledgeIsland to be evaluated.
            model (str, optional): The code of the model indicated.
            qpu (str, optional): The code of the backend QPU.

        Raises:
            ValueError: In case a specified knowledge island is not part of the QRBS or an evaluated knowledge island requires more qubits than supported.
        """
        if eval_islands is None:
            eval_islands = []
        evaluation = True
        # Initiate islands in case of specified evaluation
        if not eval_islands:
            eval_islands = qrbs._engine._islands
        else:
            for island in eval_islands:
                if island not in qrbs._engine._islands:
                    raise ValueError('A specified KnowledgeIsland is not part of the QRBS', island)
        # Build each island
        builder = SelectableQPU.BUILDERS[model]
        eval_islands = [builder.build_island(island) for island in eval_islands]
        # Check their arity is compatible with the QPU
        for island in eval_islands:
            routine, _ = island
            if routine.arity > SelectableQPU.MAX_ARITY:
                evaluation = False
                raise ValueError('A KnowledgeIsland surpasses capacity of QPU ({} qubits)'.format(
                    SelectableQPU.MAX_ARITY), qrbs._engine._islands[eval_islands.index(island)])
        return evaluation

    @staticmethod
    def execute(qrbs, islands=None, model='cf', qpu=None, shots=None) -> None:
        """Executes the QRBS on this QPU.

        Args:
            qrbs (:obj:`QRBS`): The QRBS to be executed.
            islands (List[:obj:`~neasqc_qrbs.knowledge_rep.KnowledgeIsland`], optional): A list of specific KnowledgeIsland to be executed.
            model (str, optional): The code of the model indicated.
            qpu (str, optional): The code of the backend QPU.
        """
        # Select builder
        if islands is None:
            islands = []
        builder = SelectableQPU.BUILDERS[model]
        # Initiate islands in case of specified evaluation
        if not islands:
            islands = qrbs._engine._islands
        # If evaluation is successful, continue with execution
        if SelectableQPU.evaluate(qrbs, islands, model, qpu):
            if qpu is None:
                raise ValueError("QPU must be provided!!")
            else:
                backend = qpu
            if shots is None:
                raise ValueError("Number of shots MUST BE provided")

            for island in islands:
                routine, elements = builder.build_island(island)

                prog = Program()
                qbits = prog.qalloc(routine.arity)
                prog.apply(routine, qbits)

                circ = prog.to_circ()
                job = circ.to_job(nbshots=shots)
                result = backend.submit(job)

                for element, index in elements.items():
                    if element in [rule.right_hand_side for rule in qrbs._engine._rules]:
                        temp = 0
                        for sample in result:
                            if sample.state.bitstring[index] == '1':
                                temp += sample.probability
                        temp = min(1.0, temp)
                        temp = max(0.0, temp)
                        element.precision = temp
