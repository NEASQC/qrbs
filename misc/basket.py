
import sys
import numpy as np

sys.path.append("../")
from neasqc_qrbs.qrbs import QRBS
from neasqc_qrbs.knowledge_rep import AndOperator, OrOperator, NotOperator

def degree_of_membership(x_value, def_linear_picewise):
    """
    Computes the degree of membership to a picewise lineal function for
    an input value

    Parameters
    ----------

    x_value : float
        Point of the domain for computing the degree of membership
    def_linear_picewise : str
        string for definin the linear picewise function in the format:
        "y0/x0-y1/x1-y2/x2-...-yf/xf". Example:"0/11-1/13-1/15-0/17"

    Returns
    -------

    degree : float
        degree of mebership of the input value to the defined linear
        picewise function

    """
    list_ = def_linear_picewise.split("-")
    for i in range(len(list_)-1):
        str_start = list_[i]
        x_0 = float(str_start.split("/")[1])
        y_0 = float(str_start.split("/")[0])
        if (i == 0) and (x_value <= x_0):
            return y_0
        str_end = list_[i+1]
        x_1 = float(str_end.split("/")[1])
        y_1 = float(str_end.split("/")[0])
        if (x_value >= x_0) and (x_value <= x_1):
            slope = (y_1 - y_0) / (x_1 - x_0)
            intercept = y_1 - slope * x_1
            return slope * x_value + intercept
    return y_1

def get_membership_function(domain, def_linear_picewise):
    """
    Computes for an input domain the corresponding linear picewise
    input function

    Parameters
    ----------

    domain : np.array
        numpy array with the desired domain
    def_linear_picewise : str
        string for definin the linear picewise function in the format:
        "y0/x0-y1/x1-y2/x2-...-yf/xf". Example:"0/11-1/13-1/15-0/17"

    Returns
    -------

    array : np.array
        numpy array where each element is the evaluation of the linear
        picewise function on the corresponding element of the input
        domain
    """
    list_ = def_linear_picewise.split("-")
    domain_x_0 = float(list_[0].split("/")[1])
    domain_x_f = float(list_[-1].split("/")[1])
    array = np.array(
        list(map(lambda x: degree_of_membership(x, def_linear_picewise), domain))
    )
    #array = np.where(np.array(domain) >= domain_x_0, array, np.NaN)
    #array = np.where(np.array(domain) <= domain_x_f, array, np.NaN)
    return array


def basquet_qrbs(throw, height, qpu, type_qpu=None, shots=None, model='cf', rule_certainty=1.0):
    """
    QRBS for a basket dummy problem

    Parameters
    ----------
    throw : int
        Number of target trhows (of 20)
    height : int
        Height in cm
    qpu : QLM QPU
        QLM QPU for executing the quantum circuits
    type_qpu: QLM QPU
        QLM QPU for executing the quantum circuits
    shots : int
        number of shots
    model : str
        indetermination propagation model
    """
    # Instantiate the QRBS
    basket = QRBS()
    #### Initial Facts ######
    # Free throw scoring
    throw_very_bad = basket.assert_fact("throw_very_bad", "1/0-1/3-0/7")
    throw_bad = basket.assert_fact("throw_bad", "0/3-1/5-1/7-0/9")
    throw_regular = basket.assert_fact("throw_regular", "0/7-1/10-0/13")
    throw_good = basket.assert_fact("throw_good", "0/11-1/13-1/15-0/17")
    throw_very_good = basket.assert_fact("throw_very_good", "0/15-1/17-1/20")
    # height scoring
    height_very_small = basket.assert_fact("height_very_small", "1/150-1/170-0/180")
    height_small = basket.assert_fact("height_small", "0/170-1/175-1/180-0/185")
    height_normal = basket.assert_fact("height_normal", "0/180-1/190-0/195")
    height_tall = basket.assert_fact("height_tall", "0/190-1/195-1/205-0/210")
    height_very_tall = basket.assert_fact("height_very_tall", "0/200-1/210-1/250")
    # player score
    player_bad = basket.assert_fact("player_bad", "1/0-0/1")
    player_normal = basket.assert_fact("player_normal", "1/0-1/25-0/40")
    player_good = basket.assert_fact("player_good", "0/25-1/40-1/60-0/75")
    player_very_good = basket.assert_fact("player_very_good", "0/60-1/75-1/100")
    output = [player_bad, player_normal, player_good, player_very_good]
    ###### RULES ######
    #rule_certainty = 0.8
    # Rule for normal player
    normal_0 = AndOperator(height_normal, throw_good)
    normal_1 = AndOperator(height_normal, throw_very_good)
    normal_2 = AndOperator(height_tall, throw_regular)
    normal_3 = AndOperator(height_very_tall, throw_regular)
    normal_f = OrOperator(
        OrOperator(
            OrOperator(normal_0, normal_1),
            normal_2),
        normal_3)
    rule_1 = basket.assert_rule(normal_f, player_normal, rule_certainty)
    # Rule for good player
    rule_2 = basket.assert_rule(
        OrOperator(
            AndOperator(height_tall, throw_good),
            AndOperator(height_very_tall, throw_good)
        ),
        player_good,
        rule_certainty
    )
    # Rule for very good player
    rule_3 = basket.assert_rule(
        OrOperator(
            AndOperator(height_tall, throw_very_good),
            AndOperator(height_very_tall, throw_very_good)
        ),
        player_very_good,
        rule_certainty
    )
    # Rules for Bad player
    throw_bad_player = basket.assert_fact("player_bad_throw", "player with bad throw")
    rule_4 = basket.assert_rule(
        OrOperator(throw_very_bad, throw_bad),
        throw_bad_player,
        rule_certainty
    )
    small_player = basket.assert_fact("small_player", "player too small")
    rule_5 = basket.assert_rule(
        OrOperator(height_very_small, height_small),
        small_player,
        rule_certainty
    )
    normal_regular = basket.assert_fact("normal_regular", "Normal height and regular throw")
    rule_6 = basket.assert_rule(
        AndOperator(height_normal, throw_regular),
        normal_regular,
        rule_certainty
    )
    rule_bad_player = basket.assert_rule(
        OrOperator(
            OrOperator(throw_bad_player, small_player),
            normal_regular
        ),
        player_bad,
        rule_certainty
    )
    ####### KNOWLEDGE iSLANDS ################
    island_normal = basket.assert_island([rule_1])
    island_good = basket.assert_island([rule_2])
    island_very_good = basket.assert_island([rule_3])
    island_bad = basket.assert_island([rule_4, rule_5, rule_6, rule_bad_player])
    ####### LOADING DATA #########################
    # Score data
    list_score = [throw_very_bad, throw_bad, throw_regular, throw_good, throw_very_good]
    # print([fact.precision for fact in list_score])
    for fact in list_score:
        fact.precision = degree_of_membership(throw, fact.value)
    # print([fact.precision for fact in list_score])
    # Height data
    # Asigning the precision of the facts
    list_height = [height_very_small, height_small, height_normal, height_tall, height_very_tall]
    # print([fact.precision for fact in list_height])
    for fact in list_height:
        fact.precision = degree_of_membership(height, fact.value)
    # print([fact.precision for fact in list_height])
    # Inference Execution
    qpu.execute(basket, qpu=type_qpu, shots=shots, model=model)
    # Output post processing
    #output_precision = [fact.precision for fact in output]
    additional_info = [throw_bad_player, small_player, normal_regular]
    score_domain = np.array(range(0, 101))

    # Computing degree of membership for each output fact for the input player
    degree_of_memberships = []
    for output_fact in output:
        membership_function = get_membership_function(score_domain, output_fact.value)
        player_output = np.where(membership_function < output_fact.precision, membership_function, output_fact.precision)
        player_output = np.where(np.isnan(membership_function), np.nan, player_output)
        degree_of_memberships.append(player_output)
    # Aggregation of the rules
    z = np.nanmax(np.array(degree_of_memberships), axis=0)
    # Final score
    final_score = np.sum(z * score_domain) / np.sum(z)
    output_dict = {
        "output_facts" : output,
        "additional_facts" : additional_info,
        "degree_of_memberships": degree_of_memberships,
        "z": z,
        "final_score":final_score,
        "qrbs": basket
    }
    return output_dict

