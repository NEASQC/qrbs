import sys
import pandas as pd
from qpu.select_qpu import select_qpu
from qpu.benchmark_utils import combination_for_list
from selectable_qpu import SelectableQPU
from basket import basquet_qrbs

def to_pdf(qpu_cfg):
    lista = [
        "qpu_type", "qpu_name", "kak_compiler", "sim_method", "n_samples",
        "t_gate_1qb", "t_gate_2qbs", "t_readout"]
    qpu_data = [qpu_cfg[element] for element in  lista]
    qpu_pdf = pd.DataFrame(qpu_data, index=lista).T
    qpu_pdf["depol_channel"] = qpu_cfg["depol_channel"]["active"]
    qpu_pdf["error_gate_1qb"] = qpu_cfg["depol_channel"]["error_gate_1qb"]   
    qpu_pdf["error_gate_2qbs"] = qpu_cfg["depol_channel"]["error_gate_2qbs"]   
    qpu_pdf["amplitude_damping"] = qpu_cfg["idle"]["amplitude_damping"]
    qpu_pdf["t1"] = qpu_cfg["idle"]["t1"]    
    qpu_pdf["dephasing_channel"] = qpu_cfg["idle"]["dephasing_channel"]    
    qpu_pdf["t2"] = qpu_cfg["idle"]["t2"] 
    qpu_pdf["meas"] = qpu_cfg["meas"]["active"] 
    qpu_pdf["readout_error"] = qpu_cfg["meas"]["readout_error"]     
        
    return qpu_pdf

def save(save, save_name, input_pdf, save_mode):
    """
    For saving panda DataFrames to csvs

    Parameters
    ----------

    save: bool
        For saving or not
    save_nam: str
        name for file
    input_pdf: pandas DataFrame
    save_mode: str
        saving mode: overwrite (w) or append (a)
    """
    if save:
        with open(save_name, save_mode) as f_pointer:
            input_pdf.to_csv(
                f_pointer,
                mode=save_mode,
                header=f_pointer.tell() == 0,
                sep=';'
            )

def run_id(**kwargs):
    """
    Execute the inference 
    """
    
    # Get configuration
    model = kwargs.get("model", "cf")
    print(model)
    shots = kwargs.get("shots", 0)
    qpu_cfg = kwargs.get("qpu_cfg")
    folder = kwargs.get("folder_path")
    name = kwargs.get("base_name")
    save_ = kwargs.get("save")
    # Create the file name
    file_name = folder + name + "_" + str(kwargs.get("id")) + ".csv"
    # Transform qpu configuration to Pandas 
    qpu_pdf = to_pdf(cfg["qpu_cfg"])
    qpu_pdf["model"] = model
    qpu_pdf["shots"] = shots
    # Create QPU
    qpu = select_qpu(qpu_cfg)

    # Players
    Name = ["Elias" , "Blas", "Luis", "Juan", "Raul", "Cholo"]
    Throws = [16, 17, 17, 15, 18, 18]
    Heights = [198, 193, 188, 203, 176, 186]
    
    # Create qpu for inference
    qpu_selected = SelectableQPU()
    # Player Evaluation Time
    player_evaluation= [
        basquet_qrbs(
            t, h, qpu_selected, type_qpu=qpu, shots=shots, model=model) 
                for t, h in zip(Throws, Heights)
    ]
    # Getting the scores
    pdf = [
        [n, t, h, p["final_score"]] for n, t, h, p in zip(
            Name, Throws, Heights, player_evaluation)
    ]
    pdf = pd.DataFrame(
        pdf,
        columns = ["Name", "Throws", "Height", "Final_Score"]
    )
    pdf.sort_values(["Final_Score"], ascending=False, inplace=True)
    pdf.reset_index(drop=True, inplace=True)
    # Added the qpu info
    qpu_pdf = pd.concat([qpu_pdf] * len(pdf))
    qpu_pdf.reset_index(drop=True, inplace=True)
    pdf = pd.concat([qpu_pdf, pdf], axis = 1)
    # Save
    save(save_, file_name, pdf, "w")
    return pdf

if __name__ == "__main__":
    import json
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-json_qpu",
        dest="json_qpu",
        type=str,
        default="jsons/qpu_ideal.json",
        help="JSON with the qpu configuration",
    )
    parser.add_argument(
        "-model",
        dest="model",
        type=str,
        default="cf",
        help="cf, bayes, fuzzy",
    )
    parser.add_argument(
        "-id",
        dest="id",
        type=int,
        help="For executing only one element of the list",
        default=None,
    )
    parser.add_argument(
        "-shots",
        dest="shots",
        type=int,
        help="For executing only one element of the list",
        default=0,
    )
    parser.add_argument(
        "-name",
        dest="base_name",
        type=str,
        help="Additional name for the generated files",
        default="basket_qrbs",
    )
    parser.add_argument(
        "--count",
        dest="count",
        default=False,
        action="store_true",
        help="For counting elements on the list",
    )
    parser.add_argument(
        "--all",
        dest="all",
        default=False,
        action="store_true",
        help="For executing complete list",
    )
    parser.add_argument(
        "--print",
        dest="print",
        default=False,
        action="store_true",
        help="For printing the AE algorihtm configuration."
    )
    parser.add_argument(
        "--save",
        dest="save",
        default=False,
        action="store_true",
        help="For saving staff"
    )
    parser.add_argument(
        "-folder",
        dest="folder_path",
        type=str,
        help="Path for storing folder",
        default="./",
    )
    parser.add_argument(
        "--exe",
        dest="execution",
        default=False,
        action="store_true",
        help="For executing program",
    )
    args = parser.parse_args()
    with open(args.json_qpu) as json_file:
        noisy_cfg = json.load(json_file)
    qpu_list = combination_for_list(noisy_cfg)
    if args.count:
        print("Number of elements: {}".format(len(qpu_list)))
    if args.print:
        if args.id is not None:
            print(qpu_list[args.id])
        elif args.all:
            print(qpu_list)
        else:
            print("Provide -id or --all")

    if args.execution:
        if args.id is not None:
            cfg = vars(args)
            configuration = qpu_list[args.id]
            cfg.update({"qpu_cfg":configuration})
            final_pdf = run_id(**cfg)
            print(final_pdf)
            

