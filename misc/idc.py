"""
QRBS implementation of a  IDC
"""


import sys
import itertools as it
import pandas as pd
sys.path.append("../")
from neasqc_qrbs.qrbs import QRBS
from neasqc_qrbs.knowledge_rep import AndOperator, OrOperator, NotOperator
from selectable_qpu import SelectableQPU

def idc_qrbs(row, qpu=None, shots=None, model='cf'):
    """
    QRBS implementation of the IDC
    Parameters
    ----------
    row : row of a pandas DataFrame
        input information for the idc as a pandas DataFrame row
    qpu : QLM qpu
        QLM qpu for solving the quantum circuits
    shots : int
        Number of shots for measuring the quantum circuits
    model : string
        String with the inacuracy propagation model: cf, fuzzy, bayes
    """
    idc = QRBS()
    # Setting the input facts
    # Related to tumor
    t0 = idc.assert_fact('T0', 'No evidence of tumor')
    t1 = idc.assert_fact('T1', 'Size less than or equal to 20mm')
    t2 = idc.assert_fact('T2', 'Size between 20mm and 50mm')
    t3 = idc.assert_fact('T3', 'Size greater than 50mm')
    t4 = idc.assert_fact('T4', 'Tumor involves chest wall')
    t5 = idc.assert_fact('T5', 'Tumor affects skin')
    # Related to lymphatic or auxilary nodes
    n0a = idc.assert_fact('N0A', 'Absence of cancer in lymph nodes')
    n0b = idc.assert_fact('N0B', 'Size in lymph nodes less than 0.2mm')
    n0 = OrOperator(n0a, n0b)
    n1a = idc.assert_fact('N1A', 'From 1 to 3 affected axillary lymph nodes')
    n1b = idc.assert_fact('N1B', 'Internal lymph nodes affected')
    n1 = OrOperator(n1a, n1b)
    n2a = idc.assert_fact('N2A', 'From 4 to 9 affected axillary lymph nodes')
    n2b = idc.assert_fact('N2B', 'No axillary lymph node involvement')
    n2 = OrOperator(n2a, n2b)
    n3a = idc.assert_fact('N3A', 'More than 10 affected axillary lymph nodes')
    n3b = idc.assert_fact('N3B', 'Lymph nodes below the collarbone affected')
    n3c = idc.assert_fact('N3C', 'Superclavicular lymph nodes affected')
    n3 = OrOperator(n3a, OrOperator(n3b, n3c))
    # Related to metastasis
    m0 = idc.assert_fact('M0', 'No evidence of metastasis')
    m1 = idc.assert_fact('M1', 'Cancer cells in other organs')
    inputs = [
        t0, t1, t2, t3, t4, t5,
        n0a, n0b, n1a, n1b, n2a, n2b, n3a, n3b, n3c,
        m0, m1
    ]
    # Fixed the precision of each input fact
    for i in inputs:
        i.precision = row[i.attribute]

    # Combination of input facts for creating TNM staging system
    t1n0m0 = AndOperator(t1, AndOperator(n0, m0))
    t0n1m0 = AndOperator(t0, AndOperator(n1, m0))
    t1n1m0 = AndOperator(t1, AndOperator(n1, m0))
    t2n0m0 = AndOperator(t2, AndOperator(n0, m0))
    t2n1m0 = AndOperator(t2, AndOperator(n1, m0))
    t3n0m0 = AndOperator(t3, AndOperator(n0, m0))
    t0n2m0 = AndOperator(t0, AndOperator(n2, m0))
    t1n2m0 = AndOperator(t1, AndOperator(n2, m0))
    t3n2m0 = AndOperator(t3, AndOperator(n2, m0))
    t3n1m0 = AndOperator(t3, AndOperator(n1, m0))
    t4n0m0 = AndOperator(t4, AndOperator(n0, m0))
    t4n1m0 = AndOperator(t4, AndOperator(n1, m0))
    t4n2m0 = AndOperator(t4, AndOperator(n2, m0))
    txn3m0 = AndOperator(n3, m0)
    txnym1 = m1
    # Output facts
    ia = idc.assert_fact('IA', 'Stage I-A')
    ib = idc.assert_fact('IB', 'Stage I-B')
    iia = idc.assert_fact('IIA', 'Stage II-A')
    iib = idc.assert_fact('IIB', 'Stage II-B')
    iiia = idc.assert_fact('IIIA', 'Stage III-A')
    iiib = idc.assert_fact('IIIB', 'Stage III-B')
    iiic = idc.assert_fact('IIIC', 'Stage III-C')
    iv = idc.assert_fact('IV', 'Stage IV')
    outputs = [ia, ib, iia, iib, iiia, iiib, iiic, iv]
    # Rules of the IDC
    rule_ia = idc.assert_rule(t1n0m0, ia, 1.0)
    rule_ib = idc.assert_rule(OrOperator(t0n1m0, t1n1m0), ib, 1.0)
    rule_iia = idc.assert_rule(
        OrOperator(t0n1m0, OrOperator(t1n1m0, t2n0m0)), iia, 1.0)
    rule_iib = idc.assert_rule(OrOperator(t2n1m0, t3n0m0), iib, 1.0)
    rule_iiia = idc.assert_rule(
        OrOperator(
            t0n2m0,
            OrOperator(
                OrOperator(t1n2m0, t2n0m0),
                OrOperator(t3n2m0, t3n1m0)
            )
        ),
        iiia,
        1.0
    )
    rule_iiib = idc.assert_rule(
        OrOperator(t4n0m0, OrOperator(t4n1m0, t4n2m0)), iiib, 1.0)
    rule_iiic = idc.assert_rule(txn3m0, iiic, 1.0)
    rule_iv = idc.assert_rule(txnym1, iv, 1.0)

    # Defining the islands
    staging_ia = idc.assert_island([rule_ia])
    staging_ib = idc.assert_island([rule_ib])
    staging_iia = idc.assert_island([rule_iia])
    staging_iib = idc.assert_island([rule_iib])
    staging_iiia = idc.assert_island([rule_iiia])
    staging_iiib = idc.assert_island([rule_iiib])
    staging_iiic = idc.assert_island([rule_iiic])
    staging_iv = idc.assert_island([rule_iv])

    inference_engine = SelectableQPU()

    inference_engine.execute(idc, qpu=qpu, shots=shots, model=model)
    data = [out.precision for out in outputs]
    columns = [
        "Stage I-A", "Stage I-B", "Stage II-A", "Stage II-B",
        "Stage III-A", "Stage III-B", "Stage III-C", "Stage IV"
    ]
    pdf = pd.DataFrame(data, index=columns).T
    return pdf

def create_tmn(tmn, pdf):
    """
    Give a TNM classification selects the corresponding inputs from
    DataFrame

    Parameters
    ----------
    tmn : string
        TMN input
    pdf: pandas DataFrame
        DataFrame with all possible inputs for IDC

    Return
    ------
    final : pandas DataFrame
        pandas DataFrame with the inputs corresponding to the input TMN
    """
    lista = []
    for i, cl  in enumerate(tmn.split(" ")):
        try:
            a_ = int(cl[1])
            step = [cl]
        except ValueError:
            if cl[0] == "T":
                step = ["T"+str(i) for i in range(6)]
            if cl[0] == "N":
                step = ["N0A", "N0B", "N1A", "N1B", "N2A", "N2B", "N3A", "N3B", "N3C"]
            if cl[0] == "M":
                step = ["M0", "M1"]
        lista.append(step)
    final_tmns = [" ".join(a_) for a_ in list(
        it.product(lista[0], lista[1], lista[2]))]
    final = [get_tmn_input(tmn_, pdf) for tmn_ in final_tmns]
    final = pd.concat(final)
    final["tmn"] = tmn
    return final


def get_tmn_input(tmn, pdf):
    """
    Give a TNM classification selects the corresponding inputs from
    DataFrame

    Parameters
    ----------
    tmn : string
        TMN input
    pdf: pandas DataFrame
        DataFrame with all possible inputs for IDC

    Return
    ------
    final : pandas DataFrame
        pandas DataFrame with the inputs corresponding to the input TMN
    """
    lista = []
    for i, cl  in enumerate(tmn.split(" ")):
        for j, name_ in enumerate(pdf.columns[pdf.columns.str.contains(cl)]):
            if j == 0:
                step = (pdf[name_] == 1.0)
            else:
                step = step | (pdf[name_] == 1.0)
        if i == 0:
            final = step
        else:
            final = final & step
    return pdf[final]

def prepare_input():
    """
    Prepare all posible input combinations for IDC QRBS system as a
    pandas DataFrame
    Return
    ------

    idc_df : pandas DataFrame
        DataFrame with all posible inputs for QRBS idc
    """
    #Posible t values
    t_ = [[float(i == j) for i in range(6)] for j in range(5)]
    #Posible n values
    n_ = [[float(i == j) for i in range(9)] for j in range(9)]
    m_ = [[int(i == j) for i in range(2)] for j in range(2)]
    data = [list(it.chain.from_iterable(i)) for i in it.product(t_, n_, m_)]
    columns = [
        'T0', 'T1', 'T2', 'T3', 'T4', 'T5',
        'N0A', 'N0B', 'N1A', 'N1B', 'N2A', 'N2B', 'N3A', 'N3B', 'N3C',
        'M0', 'M1'
    ]
    idc_df = pd.DataFrame(data, columns=columns)

    tmn_compatible = [
        "T1 N0 M0", "T0 N1 M0", "T1 N1 M0", "T0 N1 M0", "T1 N1 M0", "T2 N0 M0",
        "T2 N1 M0", "T3 N0 M0", "T0 N2 M0", "T1 N2 M0", "T2 N0 M0", "T3 N2 M0",
        "T3 N1 M0", "T4 N0 M0", "T4 N1 M0", "T4 N2 M0", "TX N3 M0", "TX NY M1"]

    tmn_final = pd.concat([create_tmn(tmn, idc_df) for tmn in tmn_compatible])

    return tmn_final

def exe(qpu, shots, model):
    tmn_final = prepare_input()
    lista = []
    for row in tmn_final[:2].iterrows():
        print(idc_qrbs(row[1], qpu, shots, model))

if __name__ == "__main__":
    import argparse
    import json
    import sys
    sys.path.append("../")
    from qpu.select_qpu import select_qpu
    from qpu.benchmark_utils import combination_for_list
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--count",
        dest="count",
        default=False,
        action="store_true",
        help="For counting elements on the list",
    )
    parser.add_argument(
        "-qpu",
        dest="qpu",
        type=str,
        default=None,
        help="QPU for executing the quantum circuits"
    )
    parser.add_argument(
        "-id",
        dest="id",
        type=int,
        help="For selecting the desired qpu",
        default=None,
    )
    parser.add_argument(
        "--print",
        dest="print",
        default=False,
        action="store_true",
        help="For printing "
    )
    parser.add_argument(
        "--exe",
        dest="execution",
        default=False,
        action="store_true",
        help="For executing program",
    )
    args = parser.parse_args()

    # Loading QLM QPU for optimize inferential circuit
    with open(args.qpu) as json_file:
        qpu_cfg = json.load(json_file)
    final_list = combination_for_list(qpu_cfg)
    if args.count:
        print(len(final_list))
    if args.print:
        if args.id is not None:
            print(final_list[args.id])
        else:
            print(final_list)
    if args.execution:
        if args.id is not None:
            qpu = select_qpu(final_list[args.id])
            exe(qpu, 100, "cf")
