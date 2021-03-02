# Functions module for Paisa simulation
import numpy as np
import numpy_financial as npf
import time


def api_run_simulation(input_data_form):
    # Loan grade from the frontend form
    # loan_grade = input_data_form["loan_grade"]
    loan_grade = "ALL"

    if loan_grade == "ALL":
        # Run the code with all loan grades (A to D)
        output_data_A = simulation_or_model(input_data_form, "A")
        output_data_B = simulation_or_model(input_data_form, "B")
        output_data_C = simulation_or_model(input_data_form, "C")
        output_data_D = simulation_or_model(input_data_form, "D")

        # Return the outputs
        output_data = {}
        output_data["output_data_A"] = output_data_A
        output_data["output_data_B"] = output_data_B
        output_data["output_data_C"] = output_data_C
        output_data["output_data_D"] = output_data_D

        return output_data
    else:
        # Run the code with the given loan grade (A, B, C, D, MIX)
        output_data = simulation_or_model(input_data_form, loan_grade)

        # Return the outputs
        return output_data


def simulation_or_model(input_data_form, loan_grade):
    scenario_flag = input_data_form["scenario_flag"]
    default_flag = input_data_form["default_flag"]

    if scenario_flag == 1:
        # General scenario - run current and Paisa models models for the given loan grade
        # Get the corresponding monthly defaults array
        if default_flag == "off":
            # No defaults case - an array with all zeros
            monthly_default_array = monthly_defaults_3yr()
        elif default_flag == "auto":
            # Average defaults case - array based on loan grade
            monthly_default_array = monthly_defaults_3yr(loan_grade)

        # Run current platform model
        current_output_data = current_model(
            input_data_form, loan_grade, monthly_default_array
        )

        # Run Paisa platform model
        paisa_output_data = paisa_model(
            input_data_form, loan_grade, monthly_default_array
        )

        # Output data dict
        output_data = {}
        # Paisa outputs
        output_data["paisa_abs_return_mean"] = paisa_output_data["paisa_abs_return"]
        output_data["paisa_llr_mean"] = paisa_output_data["paisa_llr"]
        output_data["paisa_lrr_mean"] = paisa_output_data["paisa_lrr"]
        output_data["paisa_abs_return_std"] = [0] * 5
        output_data["paisa_llr_std"] = [0] * 5
        output_data["paisa_lrr_std"] = [0] * 5
        # Current outputs
        output_data["current_abs_return"] = current_output_data["current_abs_return"]
        output_data["current_llr"] = current_output_data["current_llr"]
        output_data["current_lrr"] = current_output_data["current_lrr"]
    elif scenario_flag == 2 or scenario_flag == 3:
        # Load the saved scenario results
        # Paisa saved results
        saved_paisa_output_data = np.load(f"results/s{scenario_flag}_{loan_grade}.npz")

        # Run current platform model
        monthly_default_array = monthly_defaults_3yr(loan_grade)
        current_output_data = current_model(
            input_data_form, loan_grade, monthly_default_array
        )

        # Output data dict
        output_data = {}
        # Paisa outputs
        output_data["paisa_abs_return_mean"] = saved_paisa_output_data[
            "paisa_abs_return_mean"
        ]
        output_data["paisa_abs_return_std"] = saved_paisa_output_data[
            "paisa_abs_return_std"
        ]
        output_data["paisa_llr_mean"] = saved_paisa_output_data["paisa_llr_mean"]
        output_data["paisa_llr_std"] = saved_paisa_output_data["paisa_llr_std"]
        output_data["paisa_lrr_mean"] = saved_paisa_output_data["paisa_lrr_mean"]
        output_data["paisa_lrr_std"] = saved_paisa_output_data["paisa_lrr_std"]
        # Current outputs
        output_data["current_abs_return"] = current_output_data["current_abs_return"]
        output_data["current_llr"] = current_output_data["current_llr"]
        output_data["current_lrr"] = current_output_data["current_lrr"]
    elif scenario_flag == 4:
        # Custom scenario
        # Run the Paisa model simulation for the given loan grade
        # (generate random defaults with the given custom setting)
        (
            _,
            _,
            paisa_abs_return_mean,
            paisa_abs_return_std,
            paisa_llr_mean,
            paisa_llr_std,
            paisa_lrr_mean,
            paisa_lrr_std,
        ) = run_paisa_simulation(input_data_form, loan_grade)

        # Run current platform model
        current_output_data = current_model(
            input_data_form, loan_grade, monthly_defaults_3yr(loan_grade)
        )

        # Output data dict
        output_data = {}
        # Paisa outputs
        output_data["paisa_abs_return_mean"] = paisa_abs_return_mean.tolist()
        output_data["paisa_abs_return_std"] = paisa_abs_return_std.tolist()
        output_data["paisa_llr_mean"] = paisa_llr_mean.tolist()
        output_data["paisa_llr_std"] = paisa_llr_std.tolist()
        output_data["paisa_lrr_mean"] = paisa_lrr_mean.tolist()
        output_data["paisa_lrr_std"] = paisa_lrr_std.tolist()
        # Current outputs
        output_data["current_abs_return"] = current_output_data["current_abs_return"]
        output_data["current_llr"] = current_output_data["current_llr"]
        output_data["current_lrr"] = current_output_data["current_lrr"]

    # Return the outputs
    return output_data


def run_paisa_simulation(input_data_form, loan_grade, num_samples=None):
    # Inputs from the input form
    inv_time_periods_yrs = input_data_form["inv_time_periods_yrs"]
    default_mean_deviate_percent = input_data_form["default_deviate_percent"]

    # Number of simulation samples (runs)
    if num_samples is None:
        num_samples = 100

    print(f"Paisa simulation started... (Grade {loan_grade} loans)")

    # Generate the defaults from the average defaults
    # Mean vector
    default_mean_array = monthly_defaults_3yr(loan_grade)
    default_mean_array = (
        1 + (default_mean_deviate_percent / 100)
    ) * default_mean_array[1:]

    # Covariance matrix
    default_std_deviate_percent = 10
    default_variance_array = (
        (default_std_deviate_percent / 100) * default_mean_array
    ) ** 2
    cov_default_mtx = default_variance_array * np.eye(36)

    # Generate default arrays from the normal distribution
    defaults_mtx = np.random.multivariate_normal(
        default_mean_array, cov_default_mtx, num_samples
    )

    # Check for validity of generated default arrays
    valid_idx = []
    array_36_zeros = np.zeros(36)
    for i in range(num_samples):
        # defaults_array = z_scores * sigma_valid[i] + mu_valid[i]
        defaults_array = defaults_mtx[i, :]

        # Replace negative values with zeros
        defaults_array = np.maximum(defaults_array, array_36_zeros)

        # Check for validity (sum <= 1)
        if np.sum(defaults_array) <= 1:
            defaults_mtx[i, :] = defaults_array
            valid_idx.append(i)

    # Calculate Paisa KPIs for each default array
    num_valid_samples = len(valid_idx)
    num_inv_time_periods = len(inv_time_periods_yrs)

    # Initialize the output matrices
    paisa_abs_return_mtx = np.zeros((num_valid_samples, num_inv_time_periods))
    paisa_llr_mtx = np.zeros((num_valid_samples, num_inv_time_periods))
    paisa_lrr_mtx = np.zeros((num_valid_samples, num_inv_time_periods))

    for i in range(num_valid_samples):
        # Get the valid default array from the random defaults matrix
        default_array = defaults_mtx[valid_idx[i], :]

        # Insert the dummy element at the beginning
        default_array = np.insert(default_array, 0, 999)

        tic = time.perf_counter()
        # Paisa model output with the current default array
        paisa_output = paisa_model(input_data_form, loan_grade, default_array)
        toc = time.perf_counter()

        print(
            f"Run #{i+1} of {num_valid_samples} done. Time: {toc - tic:0.2f} seconds."
        )

        # Store the current output in output matrices
        paisa_abs_return_mtx[i, :] = paisa_output["paisa_abs_return"]
        paisa_llr_mtx[i, :] = paisa_output["paisa_llr"]
        paisa_lrr_mtx[i, :] = paisa_output["paisa_lrr"]

    # Compute the mean of KPIs
    paisa_abs_return_mean = np.mean(paisa_abs_return_mtx, axis=0)
    paisa_llr_mean = np.mean(paisa_llr_mtx, axis=0)
    paisa_lrr_mean = np.mean(paisa_lrr_mtx, axis=0)

    # Compute the standard deviation of KPIs
    paisa_abs_return_std = np.std(paisa_abs_return_mtx, axis=0)
    paisa_llr_std = np.std(paisa_llr_mtx, axis=0)
    paisa_lrr_std = np.std(paisa_lrr_mtx, axis=0)

    # Generated defaults matrix
    defaults_mtx_valid = defaults_mtx[valid_idx, :]

    # Return the outputs
    return (
        defaults_mtx_valid,
        paisa_abs_return_mtx,
        paisa_abs_return_mean,
        paisa_abs_return_std,
        paisa_llr_mean,
        paisa_llr_std,
        paisa_lrr_mean,
        paisa_lrr_std,
    )


def paisa_model(input_data_form, loan_grade, monthly_default_array):
    # Inputs from the frontend form
    # Primary inputs
    # paisa_interest_percent = input_data_form["paisa_interest_percent"]

    # Investment time periods (in years)
    inv_time_periods_yrs = input_data_form["inv_time_periods_yrs"]

    # Platform's revenue percentages
    paisa_orig_percent = input_data_form["paisa_orig_percent"]
    paisa_comm_percent = input_data_form["paisa_comm_percent"]

    # Reinvestment periods
    paisa_emi_reinvest_period = input_data_form["emi_reinvest_period"]

    # Initial principal stats
    principal = input_data_form["principal"]

    #######################################################################
    # Fixed inputs
    principal_grow_percent = -100
    # Percent of accumulated EMI reinvested
    emi_reinvest_percent = 100
    # Principal reinvestment percent (for Paisa platform)
    principal_reinvest_percent = 100
    # Annual interest rate - input or take based on the loan grade
    paisa_annual_intr_percent = annual_interest_3yr(loan_grade)
    # if paisa_interest_percent:
    #     paisa_annual_intr_percent = paisa_interest_percent
    # else:
    #     paisa_annual_intr_percent = annual_interest_3yr(loan_grade)

    #######################################################################
    # Run the code with above inputs
    # Loop over the given investment periods
    paisa_abs_return = []
    paisa_abs_return_sec = []
    paisa_llr = []
    paisa_lrr = []
    # paisa_principal_leftover = []
    # paisa_mtx_lending = []
    # paisa_mtx_emi = []
    # paisa_mtx_principal_left = []
    for inv_time_period in inv_time_periods_yrs:
        (
            _,
            paisa_abs_return_val,
            _,
            paisa_abs_return_sec_val,
            paisa_llr_val,
            paisa_lrr_val,
            _,
        ) = paisa_platform(
            principal,
            paisa_annual_intr_percent,
            inv_time_period * 12,
            principal_grow_percent,
            paisa_emi_reinvest_period,
            emi_reinvest_percent,
            principal_reinvest_percent,
            paisa_orig_percent,
            paisa_comm_percent,
            monthly_default_array,
        )

        # Append the new values
        paisa_abs_return.append(paisa_abs_return_val)
        paisa_abs_return_sec.append(paisa_abs_return_sec_val)
        paisa_llr.append(paisa_llr_val)
        paisa_lrr.append(paisa_lrr_val)

    # Return the outputs
    output_data = {}
    output_data["paisa_abs_return"] = paisa_abs_return
    output_data["paisa_abs_return_sec"] = paisa_abs_return_sec
    output_data["paisa_llr"] = paisa_llr
    output_data["paisa_lrr"] = paisa_lrr

    return output_data


def current_model(input_data_form, loan_grade, monthly_default_array):
    # Inputs from the frontend form
    # Primary inputs
    # current_interest_percent = input_data_form["current_interest_percent"]

    # Investment time periods (in years)
    inv_time_periods_yrs = input_data_form["inv_time_periods_yrs"]

    # Current platform's revenue percentages
    current_orig_percent = input_data_form["current_orig_percent"]
    current_comm_percent = input_data_form["current_comm_percent"]

    # Reinvestment periods
    current_emi_reinvest_period = input_data_form["emi_reinvest_period"]

    # Initial principal stats
    principal = input_data_form["principal"]

    #######################################################################
    # Fixed inputs
    principal_grow_percent = -100
    # Percent of accumulated EMI reinvested
    emi_reinvest_percent = 100
    # Annual interest rate - input or take based on the loan grade
    current_annual_intr_percent = annual_interest_3yr(loan_grade)
    # if current_interest_percent:
    #     current_annual_intr_percent = current_interest_percent
    # else:
    #     current_annual_intr_percent = annual_interest_3yr(loan_grade)

    #######################################################################
    # Run the code with above inputs
    # Loop over the given investment periods
    current_abs_return = []
    current_llr = []
    current_lrr = []
    # current_mtx_lending = []
    # current_mtx_emi = []
    # current_mtx_principal_left = []
    # current_mtx_interest_paid = []
    for inv_time_period in inv_time_periods_yrs:
        (
            _,
            current_abs_return_val,
            current_llr_val,
            current_lrr_val,
        ) = current_platform(
            principal,
            current_annual_intr_percent,
            inv_time_period * 12,
            principal_grow_percent,
            current_emi_reinvest_period,
            emi_reinvest_percent,
            current_orig_percent,
            current_comm_percent,
            monthly_default_array,
        )

        # Append the new values
        current_abs_return.append(current_abs_return_val)
        current_llr.append(current_llr_val)
        current_lrr.append(current_lrr_val)

    #######################################################################
    # Return the outputs
    output_data = {}
    output_data["current_abs_return"] = current_abs_return
    output_data["current_llr"] = current_llr
    output_data["current_lrr"] = current_lrr

    return output_data


def annual_interest_3yr(loan_grade):
    if loan_grade == "MIX":
        annual_interest_percent = 12.32
    elif loan_grade == "A":
        annual_interest_percent = 7.17
    elif loan_grade == "B":
        annual_interest_percent = 10.78
    elif loan_grade == "C":
        annual_interest_percent = 14.29
    elif loan_grade == "D":
        annual_interest_percent = 18.43

    return annual_interest_percent


def monthly_defaults_3yr(loan_grade=None):
    if loan_grade is None:
        # No defaults case - Return an array with all zeros
        monthly_defaults_array = np.zeros(37)
    elif loan_grade == "MIX":
        monthly_default_percent = [
            99999,
            0.00,
            0.00,
            0.00,
            0.00,
            0.10,
            0.10,
            0.20,
            0.20,
            0.20,
            0.30,
            0.40,
            0.30,
            0.40,
            0.30,
            0.40,
            0.30,
            0.40,
            0.30,
            0.40,
            0.30,
            0.20,
            0.30,
            0.20,
            0.20,
            0.20,
            0.20,
            0.20,
            0.10,
            0.10,
            0.10,
            0.10,
            0.10,
            0.00,
            0.10,
            0.00,
            0.00,
        ]
        monthly_default_percent = np.array(monthly_default_percent)
        monthly_defaults_array = monthly_default_percent / 100
    elif loan_grade == "A":
        monthly_default_percent = [
            99999,
            0.00,
            0.00,
            0.00,
            0.00,
            0.00,
            0.00,
            0.10,
            0.00,
            0.10,
            0.10,
            0.10,
            0.00,
            0.20,
            0.00,
            0.10,
            0.10,
            0.20,
            0.10,
            0.10,
            0.10,
            0.10,
            0.10,
            0.10,
            0.10,
            0.10,
            0.10,
            0.00,
            0.10,
            0.00,
            0.10,
            0.00,
            0.10,
            0.00,
            0.00,
            0.00,
            0.00,
        ]
        monthly_default_percent = np.array(monthly_default_percent)
        monthly_defaults_array = monthly_default_percent / 100
    elif loan_grade == "B":
        monthly_default_percent = [
            99999,
            0.00,
            0.00,
            0.00,
            0.00,
            0.00,
            0.10,
            0.10,
            0.20,
            0.20,
            0.20,
            0.20,
            0.20,
            0.30,
            0.20,
            0.30,
            0.30,
            0.30,
            0.30,
            0.30,
            0.20,
            0.20,
            0.30,
            0.20,
            0.20,
            0.10,
            0.20,
            0.20,
            0.10,
            0.10,
            0.10,
            0.10,
            0.10,
            0.00,
            0.10,
            0.00,
            0.00,
        ]
        monthly_default_percent = np.array(monthly_default_percent)
        monthly_defaults_array = monthly_default_percent / 100
    elif loan_grade == "C":
        monthly_default_percent = [
            99999,
            0.00,
            0.00,
            0.00,
            0.00,
            0.10,
            0.10,
            0.30,
            0.30,
            0.40,
            0.50,
            0.40,
            0.50,
            0.60,
            0.60,
            0.50,
            0.60,
            0.50,
            0.50,
            0.50,
            0.40,
            0.40,
            0.40,
            0.30,
            0.30,
            0.30,
            0.20,
            0.20,
            0.20,
            0.20,
            0.10,
            0.10,
            0.10,
            0.10,
            0.10,
            0.00,
            0.00,
        ]
        monthly_default_percent = np.array(monthly_default_percent)
        monthly_defaults_array = monthly_default_percent / 100
    elif loan_grade == "D":
        monthly_default_percent = [
            99999,
            0.00,
            0.00,
            0.00,
            0.00,
            0.20,
            0.40,
            0.50,
            0.70,
            0.60,
            0.80,
            0.80,
            0.90,
            1.00,
            0.70,
            0.90,
            0.70,
            0.80,
            0.60,
            0.70,
            0.60,
            0.50,
            0.50,
            0.40,
            0.30,
            0.40,
            0.30,
            0.30,
            0.20,
            0.20,
            0.20,
            0.10,
            0.10,
            0.10,
            0.10,
            0.00,
            0.10,
        ]
        monthly_default_percent = np.array(monthly_default_percent)
        monthly_defaults_array = monthly_default_percent / 100

    # Return the default array
    return monthly_defaults_array


def monthly_defaults_3yr_mu_sig_z(loan_grade):
    if loan_grade == "MIX":
        monthly_default_mean = 0.1861 / 100
        monthly_default_sigma = 0.1334 / 100
        monthly_default_zscores = [
            99999,
            -1.3949,
            -1.3949,
            -1.3949,
            -1.3949,
            -0.6454,
            -0.6454,
            0.1041,
            0.1041,
            0.1041,
            0.8536,
            1.6031,
            0.8536,
            1.6031,
            0.8536,
            1.6031,
            0.8536,
            1.6031,
            0.8536,
            1.6031,
            0.8536,
            0.1041,
            0.8536,
            0.1041,
            0.1041,
            0.1041,
            0.1041,
            0.1041,
            -0.6454,
            -0.6454,
            -0.6454,
            -0.6454,
            -0.6454,
            -1.3949,
            -0.6454,
            -1.3949,
            -1.3949,
        ]
    elif loan_grade == "A":
        monthly_default_mean = 0.0611 / 100
        monthly_default_sigma = 0.0599 / 100
        monthly_default_zscores = [
            99999,
            -1.0203,
            -1.0203,
            -1.0203,
            -1.0203,
            -1.0203,
            -1.0203,
            0.6493,
            -1.0203,
            0.6493,
            0.6493,
            0.6493,
            -1.0203,
            2.3189,
            -1.0203,
            0.6493,
            0.6493,
            2.3189,
            0.6493,
            0.6493,
            0.6493,
            0.6493,
            0.6493,
            0.6493,
            0.6493,
            0.6493,
            0.6493,
            -1.0203,
            0.6493,
            -1.0203,
            0.6493,
            -1.0203,
            0.6493,
            -1.0203,
            -1.0203,
            -1.0203,
            -1.0203,
        ]
    elif loan_grade == "B":
        monthly_default_mean = 0.15 / 100
        monthly_default_sigma = 0.1056 / 100
        monthly_default_zscores = [
            99999,
            -1.4210,
            -1.4210,
            -1.4210,
            -1.4210,
            -1.4210,
            -0.4737,
            -0.4737,
            0.4737,
            0.4737,
            0.4737,
            0.4737,
            0.4737,
            1.4210,
            0.4737,
            1.4210,
            1.4210,
            1.4210,
            1.4210,
            1.4210,
            0.4737,
            0.4737,
            1.4210,
            0.4737,
            0.4737,
            -0.4737,
            0.4737,
            0.4737,
            -0.4737,
            -0.4737,
            -0.4737,
            -0.4737,
            -0.4737,
            -1.4210,
            -0.4737,
            -1.4210,
            -1.4210,
        ]
    elif loan_grade == "C":
        monthly_default_mean = 0.2722 / 100
        monthly_default_sigma = 0.1994 / 100
        monthly_default_zscores = [
            99999,
            -1.3649,
            -1.3649,
            -1.3649,
            -1.3649,
            -0.8635,
            -0.8635,
            0.1393,
            0.1393,
            0.6407,
            1.1421,
            0.6407,
            1.1421,
            1.6435,
            1.6435,
            1.1421,
            1.6435,
            1.1421,
            1.1421,
            1.1421,
            0.6407,
            0.6407,
            0.6407,
            0.1393,
            0.1393,
            0.1393,
            -0.3621,
            -0.3621,
            -0.3621,
            -0.3621,
            -0.8635,
            -0.8635,
            -0.8635,
            -0.8635,
            -0.8635,
            -1.3649,
            -1.3649,
        ]
    elif loan_grade == "D":
        monthly_default_mean = 0.4083 / 100
        monthly_default_sigma = 0.3065 / 100
        monthly_default_zscores = [
            99999,
            -1.3323,
            -1.3323,
            -1.3323,
            -1.3323,
            -0.6798,
            -0.0272,
            0.2991,
            0.9517,
            0.6254,
            1.2780,
            1.2780,
            1.6042,
            1.9305,
            0.9517,
            1.6042,
            0.9517,
            1.2780,
            0.6254,
            0.9517,
            0.6254,
            0.2991,
            0.2991,
            -0.0272,
            -0.3535,
            -0.0272,
            -0.3535,
            -0.3535,
            -0.6798,
            -0.6798,
            -0.6798,
            -1.0061,
            -1.0061,
            -1.0061,
            -1.0061,
            -1.3323,
            -1.0061,
        ]

    return monthly_default_mean, monthly_default_sigma, monthly_default_zscores


def loan_payments(
    principal, annual_intr_percent, duration_months, monthly_defaults_array
):

    # Monthly interest rate
    annual_intr = annual_intr_percent / 100
    monthly_intr = annual_intr / 12

    # Initialize the arrays
    months = np.arange(1, duration_months + 1)
    emi = np.zeros(duration_months + 1)
    principal_paid = np.zeros(duration_months + 1)
    principal_left = np.zeros(duration_months + 1)
    interest_paid = np.zeros(duration_months + 1)

    principal_left[0] = principal
    for month in months:
        # Current month's principal after default
        principal_curr = principal_left[month - 1] * (1 - monthly_defaults_array[month])

        # EMI
        emi[month] = -npf.pmt(
            monthly_intr, duration_months - (month - 1), principal_curr
        )

        # Principal paid
        principal_paid[month] = -npf.ppmt(
            monthly_intr, 1, duration_months - (month - 1), principal_curr
        )

        # Interest paid
        interest_paid[month] = emi[month] - principal_paid[month]

        # Principal left
        principal_left[month] = principal_curr - principal_paid[month]

    # Return outputs
    return emi, principal_paid, interest_paid, principal_left


def current_platform(
    principal,
    annual_intr_percent,
    inv_time_period,
    principal_grow_percent,
    emi_reinvest_period,
    emi_reinvest_percent,
    platform_orig_percent,
    platform_emi_percent,
    monthly_default,
):

    # Loan duration
    duration_months = 3 * 12

    # Initialize matrices
    # Row = month of loan initiation by lenders
    # Column = month of EMI received
    mtx_emi = np.zeros((inv_time_period + 1, inv_time_period + 1))
    mtx_principal_left = np.zeros((inv_time_period + 1, inv_time_period + 1))
    mtx_interest_paid = np.zeros((inv_time_period + 1, inv_time_period + 1))

    # mtx_lending matrix columns:
    # column 1 = outside principal (with a growth rate)
    # column 2 = accumulated EMIs reinvested at some frequency
    # column 3 = column 1 + column 2 = total money into the platform
    mtx_lending = np.zeros((inv_time_period + 1, 3))

    # Loop over months in rows
    mtx_lending[0, 0] = principal
    mtx_lending[0, 2] = mtx_lending[0, 0] + mtx_lending[0, 1]
    for month in range(inv_time_period - 35):

        # Current month index in column
        curr_month = month + 1

        # Get arrays from the loan payments function
        emi_arr, _, interest_paid_arr, principal_left_arr = loan_payments(
            mtx_lending[month, 2], annual_intr_percent, duration_months, monthly_default
        )

        # Matrices of EMI, principal left, interest paid
        mtx_emi[month, curr_month : curr_month + 36] = emi_arr[1:]
        mtx_principal_left[month, curr_month : curr_month + 36] = principal_left_arr[1:]
        mtx_interest_paid[month, curr_month : curr_month + 36] = interest_paid_arr[1:]

        # Run for all months, except last month
        if curr_month != inv_time_period - 35:
            mtx_lending[curr_month, 0] = mtx_lending[month, 0] * (
                1 + principal_grow_percent / 100
            )

            # Calculate accumulated EMIs reinvestment (periodically)
            if curr_month % emi_reinvest_period == 0:
                mtx_lending[curr_month, 1] = np.sum(
                    mtx_emi[:, curr_month - emi_reinvest_period + 1 : curr_month + 1]
                ) * (emi_reinvest_percent / 100)

            # Total reinvestment amounts (new monthly money in + accumulated EMIs)
            mtx_lending[curr_month, 2] = (
                mtx_lending[curr_month, 0] + mtx_lending[curr_month, 1]
            )

    ############################################################################
    # Lender returns calculations
    ############################################################################
    # Total money in
    money_in = np.sum(mtx_lending[:, 0])

    # Calculate the original investment stop month
    stop_month_money_in = np.max(np.nonzero(mtx_lending[:, 0]))

    # Calculate the EMI reinvest stop month
    x = 1
    while True:
        check_num = inv_time_period - duration_months
        if emi_reinvest_period * x > check_num:
            stop_month_emi_reinvest = emi_reinvest_period * (x - 1)
            break
        x += 1

    # Total money out
    money_out = (
        np.sum(mtx_emi[:, 0 : stop_month_emi_reinvest + 1])
        * (1 - emi_reinvest_percent / 100)
        + np.sum(mtx_emi[:, stop_month_emi_reinvest + 1 :])
        - np.sum(mtx_interest_paid) * (platform_emi_percent / annual_intr_percent)
    )

    # Average investment time period (in years)
    if emi_reinvest_percent == 0:
        avg_invest_time_yr = duration_months / 12
    else:
        weights = mtx_lending[:, 0] / money_in
        time_periods = np.zeros(stop_month_money_in + 1)
        time_periods[0] = stop_month_emi_reinvest + duration_months
        for i in range(1, stop_month_money_in + 1):
            time_periods[i] = time_periods[i - 1] - 1
            if i > stop_month_emi_reinvest:
                time_periods[i] = duration_months
        avg_invest_time_yr = (
            np.sum(weights[0 : stop_month_money_in + 1] * time_periods) / 12
        )

    # Average return per annum
    avg_return = ((money_out / money_in) ** (1 / avg_invest_time_yr) - 1) * 100

    # Total absolute return
    abs_return = ((money_out / money_in) - 1) * 100

    ############################################################################
    # Current Platform KPIs
    ############################################################################
    # Lend to loan ratio
    platform_loan_total = np.sum(mtx_lending[:, 2])
    current_llr = platform_loan_total / money_in

    # Platform revenue
    current_revenue = np.sum(mtx_interest_paid) * (
        platform_emi_percent / annual_intr_percent
    ) + platform_loan_total * (platform_orig_percent / 100)

    # Lend to platform revenue ratio
    current_lrr = (current_revenue / money_in) * 100

    ############################################################################
    # Return the function outputs
    ############################################################################
    return avg_return, abs_return, current_llr, current_lrr


def paisa_platform(
    principal,
    annual_intr_percent,
    inv_time_period,
    principal_grow_percent,
    emi_reinvest_period,
    emi_reinvest_percent,
    principal_reinvest_percent,
    platform_orig_percent,
    platform_emi_percent,
    monthly_default,
):

    # Loan duration
    duration_months = 3 * 12

    # Paisa platform split month
    split_month = 18

    # Initialize matrices
    # Row = month of loan initiation by lenders
    # Column = month of EMI received

    # Platform matrices
    # mtx_lending matrix columns:
    # column 1 = outside principal (with a growth rate)
    # column 2 = accumulated EMIs reinvested at some frequency
    # column 3 = principal taken out and reinvested (every 18 months)
    # column 4 = column 1 + column 2 + column 3
    mtx_lending = np.zeros((inv_time_period + 1, 4))

    # Primary lender matrices
    mtx_emi = np.zeros((inv_time_period + 1, inv_time_period + 1))
    mtx_principal_left = np.zeros((inv_time_period + 1, inv_time_period + 1))
    mtx_interest_paid = np.zeros((inv_time_period + 1, inv_time_period + 1))

    # Secondary partner matrices
    mtx_emi_sec = np.zeros((inv_time_period + 1, inv_time_period + 1 + split_month))
    mtx_principal_left_sec = np.zeros(
        (inv_time_period + 1, inv_time_period + 1 + split_month)
    )
    mtx_interest_paid_sec = np.zeros(
        (inv_time_period + 1, inv_time_period + 1 + split_month)
    )

    # Loop over months in rows
    mtx_lending[0, 0] = principal
    mtx_lending[0, 3] = mtx_lending[0, 0] + mtx_lending[0, 1] + mtx_lending[0, 2]
    for month in range(inv_time_period - (split_month - 1)):

        # Current month index in column
        curr_month = month + 1

        # Get arrays from the loan payments function
        emi_arr, _, interest_paid_arr, principal_left_arr = loan_payments(
            mtx_lending[month, 3], annual_intr_percent, duration_months, monthly_default
        )

        # Primary matrices of EMI, principal left, interest paid
        mtx_emi[month, curr_month : curr_month + split_month] = emi_arr[
            1 : split_month + 1
        ]
        mtx_principal_left[
            month, curr_month : curr_month + split_month
        ] = principal_left_arr[1 : split_month + 1]
        mtx_interest_paid[
            month, curr_month : curr_month + split_month
        ] = interest_paid_arr[1 : split_month + 1]

        # Secondary matrices
        mtx_emi_sec[
            month, curr_month + split_month : curr_month + 2 * split_month
        ] = emi_arr[split_month + 1 :]
        mtx_principal_left_sec[
            month, curr_month + split_month : curr_month + 2 * split_month
        ] = principal_left_arr[split_month + 1 :]
        mtx_interest_paid_sec[
            month, curr_month + split_month : curr_month + 2 * split_month
        ] = interest_paid_arr[split_month + 1 :]

        # Run for all months, except last month
        if curr_month < inv_time_period - (2 * split_month - 1):
            mtx_lending[curr_month, 0] = mtx_lending[month, 0] * (
                1 + principal_grow_percent / 100
            )

        # Don't calculate for the last month
        if curr_month < inv_time_period - (split_month - 1):
            # Calculate accumulated EMIs reinvestmen(periodically)
            if curr_month % emi_reinvest_period == 0:
                mtx_lending[curr_month, 1] = np.sum(
                    mtx_emi[:, curr_month - emi_reinvest_period + 1 : curr_month + 1]
                ) * (emi_reinvest_percent / 100)

            # Principal taken out starts after 18 months
            if curr_month >= split_month:
                mtx_lending[curr_month, 2] = mtx_principal_left[
                    curr_month - split_month, curr_month
                ] * (principal_reinvest_percent / 100)

        # Total reinvestment amounts (new monthly monein + accumulated EMIs)
        mtx_lending[curr_month, 3] = (
            mtx_lending[curr_month, 0]
            + mtx_lending[curr_month, 1]
            + mtx_lending[curr_month, 2]
        )

    ############################################################################
    # Primary lender returns calculations
    ############################################################################
    # Total money in (primary)
    money_in = np.sum(mtx_lending[:, 0])

    # Calculate the original investment stop month
    # stop_month_money_in = np.max(np.nonzero(mtx_lending[:, 0]))

    # Calculate all the leftover principals
    principal_leftover = mtx_lending[:, 2] / (principal_reinvest_percent / 100)
    for month in range(inv_time_period - (split_month - 1), inv_time_period + 1):
        principal_leftover[month] = mtx_principal_left[month - split_month, month]

    # Calculate the EMI reinvest stop month
    x = 1
    while True:
        check_num = inv_time_period - split_month
        if emi_reinvest_period * x > check_num:
            emi_reinvest_stop_month = emi_reinvest_period * (x - 1)
            break
        x += 1

    # Calculate the principal reinvest stop month
    principal_reinvest_stop_month = np.max(np.nonzero(mtx_lending[:, 2]))

    # Total money out (primary)
    money_out = (
        np.sum(mtx_emi[:, 0 : emi_reinvest_stop_month + 1])
        * (1 - emi_reinvest_percent / 100)
        + np.sum(mtx_emi[:, emi_reinvest_stop_month + 1 :])
        + np.sum(
            principal_leftover[0 : principal_reinvest_stop_month + 1]
            * (1 - principal_reinvest_percent / 100)
        )
        + np.sum(principal_leftover[principal_reinvest_stop_month + 1 :])
    ) - np.sum(mtx_interest_paid) * (platform_emi_percent / annual_intr_percent)

    # # Average investment time period (in years)
    # if principal_reinvest_percent <= 0.1:
    #     if emi_reinvest_percent == 0:
    #         # Average investment time period
    #         avg_invest_time_yr = split_month / 12
    #     else:
    #         weights = mtx_lending[:, 0] / money_in
    #         time_periods = np.zeros(stop_month_money_in + 1)
    #         time_periods[0] = (
    #             max(emi_reinvest_stop_month, principal_reinvest_stop_month)
    #             + split_month
    #         )
    #         for i in range(1, stop_month_money_in + 1):
    #             time_periods[i] = time_periods[i - 1] - 1
    #             if i > emi_reinvest_stop_month:
    #                 time_periods[i] = duration_months
    #         # Average investment time period
    #         avg_invest_time_yr = (
    #             np.sum(weights[0 : stop_month_money_in + 1] * time_periods) / 12
    #         )
    # else:
    #     weights = mtx_lending[:, 0] / money_in
    #     time_periods = np.zeros(stop_month_money_in + 1)
    #     for month in range(stop_month_money_in + 1):
    #         # Principal component invested period
    #         x = 1
    #         while True:
    #             if (month + x * split_month) > inv_time_period:
    #                 time_period_principal = (x - 1) * split_month
    #                 break
    #             x += 1
    #         # EMI component invested period
    #         if month < emi_reinvest_stop_month:
    #             time_period_emi = emi_reinvest_stop_month + split_month - month
    #             # Max of these two periods
    #             time_periods[month] = max(time_period_emi, time_period_principal)
    #         else:
    #             time_periods[month] = time_period_principal
    #     # Average investment time period
    #     avg_invest_time_yr = (
    #         np.sum(weights[0 : stop_month_money_in + 1] * time_periods) / 12
    #     )

    # # Average return per annum (primary)
    # avg_return = ((money_out / money_in) ** (1 / avg_invest_time_yr) - 1) * 100

    # Total absolute return (primary)
    abs_return = ((money_out / money_in) - 1) * 100

    ############################################################################
    # Secondary partner returns calculations
    ############################################################################
    # Total money in (secondary)
    money_in_sec = np.sum(principal_leftover)

    # Total money out (secondary)
    money_out_sec = np.sum(mtx_emi_sec) - np.sum(mtx_interest_paid_sec) * (
        platform_emi_percent / annual_intr_percent
    )

    # Average return per annum (secondary)
    avg_return_sec = ((money_out_sec / money_in_sec) ** (1 / 1.5) - 1) * 100

    # Total absolute return (secondary)
    abs_return_sec = ((money_out_sec / money_in_sec) - 1) * 100

    ############################################################################
    # Paisa Platform KPIs
    ############################################################################
    # Lend to loan ratio
    platform_loan_total = np.sum(mtx_lending[:, 3])
    paisa_llr = platform_loan_total / money_in

    # Platform revenue
    paisa_revenue = (np.sum(mtx_interest_paid) + np.sum(mtx_interest_paid_sec)) * (
        platform_emi_percent / annual_intr_percent
    ) + platform_loan_total * (platform_orig_percent / 100)

    # Lend to platform revenue ratio
    paisa_lrr = (paisa_revenue / money_in) * 100

    ############################################################################
    # Return the function outputs
    ############################################################################
    return (
        None,
        abs_return,
        avg_return_sec,
        abs_return_sec,
        paisa_llr,
        paisa_lrr,
        principal_leftover,
    )

