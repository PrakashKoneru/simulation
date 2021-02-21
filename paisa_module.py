# Functions module for Paisa simulation
import numpy as np
import numpy_financial as npf


def run_simulation(input_data_form):

    # Inputs from the frontend form
    # Primary inputs
    loan_grade = input_data_form["loan_grade"]
    inv_time_periods = input_data_form["inv_time_periods"]
    defaults_present = input_data_form["defaults_present"]

    # Platform's revenue percentages
    current_orig_percent = input_data_form["current_orig_percent"]
    current_comm_percent = input_data_form["current_comm_percent"]
    paisa_orig_percent = input_data_form["paisa_orig_percent"]
    paisa_comm_percent = input_data_form["paisa_comm_percent"]

    # Reinvestment period
    emi_reinvest_period = input_data_form["emi_reinvest_period"]

    # Initial principal
    principal = input_data_form["principal"]
    principal_grow_percent = input_data_form["principal_grow_percent"]

    #######################################################################
    # Fixed inputs
    # Percent of accumulated EMI reinvested
    emi_reinvest_percent = 100
    # Principal reinvestment percent (for Paisa platform)
    principal_reinvest_percent = 100

    #######################################################################
    # Run the code with above inputs
    # Monthly default rates based on the loan grade
    if defaults_present:
        monthly_default = monthly_defaults_3yr(loan_grade)
    else:
        # No defaults case - Returns an array with all zeros
        monthly_default = monthly_defaults_3yr()

    # Annual interest rate based on the loan grade
    annual_intr_percent = annual_interest_3yr(loan_grade)

    # Loop for plots
    current_abs_return = []
    current_llr = []
    current_lrr = []
    paisa_abs_return = []
    paisa_abs_return_sec = []
    paisa_llr = []
    paisa_lrr = []
    for inv_time_period in inv_time_periods:
        # Current platform
        (
            _,
            current_abs_return_val,
            current_llr_val,
            current_lrr_val,
        ) = current_platform(
            principal,
            annual_intr_percent,
            inv_time_period * 12,
            principal_grow_percent,
            emi_reinvest_period,
            emi_reinvest_percent,
            current_orig_percent,
            current_comm_percent,
            monthly_default,
        )

        # Append the new values
        current_abs_return.append(current_abs_return_val)
        current_llr.append(current_llr_val)
        current_lrr.append(current_lrr_val)

        # Paisa platform
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
            annual_intr_percent,
            inv_time_period * 12,
            principal_grow_percent,
            emi_reinvest_period,
            emi_reinvest_percent,
            principal_reinvest_percent,
            paisa_orig_percent,
            paisa_comm_percent,
            monthly_default,
        )

        # Append the new values
        paisa_abs_return.append(paisa_abs_return_val)
        paisa_abs_return_sec.append(paisa_abs_return_sec_val)
        paisa_llr.append(paisa_llr_val)
        paisa_lrr.append(paisa_lrr_val)

    #######################################################################
    # Return the outputs
    output_data = {}

    output_data["current_abs_return"] = current_abs_return
    output_data["current_llr"] = current_llr
    output_data["current_lrr"] = current_lrr
    output_data["paisa_abs_return"] = paisa_abs_return
    output_data["paisa_abs_return_sec"] = paisa_abs_return_sec
    output_data["paisa_llr"] = paisa_llr
    output_data["paisa_lrr"] = paisa_lrr
    
    return output_data


def annual_interest_3yr(loan_grade):
    if loan_grade == "ALL":
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
    elif loan_grade == "ALL":
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
    money_out = np.sum(mtx_emi[:, 0 : stop_month_emi_reinvest + 1]) * (
        1 - emi_reinvest_percent / 100
    ) + np.sum(mtx_emi[:, stop_month_emi_reinvest + 1 :])

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
    stop_month_money_in = np.max(np.nonzero(mtx_lending[:, 0]))

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
            principal_leftover[0 : inv_time_period - (split_month - 1)]
            * (1 - principal_reinvest_percent / 100)
        )
        + np.sum(principal_leftover[inv_time_period - (split_month - 1) :])
    )

    # Average investment time period (in years)
    if principal_reinvest_percent <= 0.1:
        if emi_reinvest_percent == 0:
            # Average investment time period
            avg_invest_time_yr = split_month / 12
        else:
            weights = mtx_lending[:, 0] / money_in
            time_periods = np.zeros(stop_month_money_in + 1)
            time_periods[0] = (
                max(emi_reinvest_stop_month, principal_reinvest_stop_month)
                + split_month
            )
            for i in range(1, stop_month_money_in + 1):
                time_periods[i] = time_periods[i - 1] - 1
                if i > emi_reinvest_stop_month:
                    time_periods[i] = duration_months
            # Average investment time period
            avg_invest_time_yr = (
                np.sum(weights[0 : stop_month_money_in + 1] * time_periods) / 12
            )
    else:
        weights = mtx_lending[:, 0] / money_in
        time_periods = np.zeros(stop_month_money_in + 1)
        for month in range(stop_month_money_in + 1):
            # Principal component invested period
            x = 1
            while True:
                if (month + x * split_month) > inv_time_period:
                    time_period_principal = (x - 1) * split_month
                    break
                x += 1
            # EMI component invested period
            if month < emi_reinvest_stop_month:
                time_period_emi = emi_reinvest_stop_month + split_month - month
                # Max of these two periods
                time_periods[month] = max(time_period_emi, time_period_principal)
            else:
                time_periods[month] = time_period_principal
        # Average investment time period
        avg_invest_time_yr = (
            np.sum(weights[0 : stop_month_money_in + 1] * time_periods) / 12
        )

    # Average return per annum (primary)
    avg_return = ((money_out / money_in) ** (1 / avg_invest_time_yr) - 1) * 100

    # Total absolute return (primary)
    abs_return = ((money_out / money_in) - 1) * 100

    ############################################################################
    # Secondary partner returns calculations
    ############################################################################
    # Total money in (secondary)
    money_in_sec = np.sum(principal_leftover)

    # Total money out (secondary)
    money_out_sec = np.sum(mtx_emi_sec)

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
        avg_return,
        abs_return,
        avg_return_sec,
        abs_return_sec,
        paisa_llr,
        paisa_lrr,
        principal_leftover,
    )

