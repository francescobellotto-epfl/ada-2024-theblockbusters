def print_missing_stats(df):
    """
    Print ratio of missing values out of total number of
    observations for each feature.

    Args:
        df: Pandas DataFrame

    """
    print("Total length:", len(df))

    for col in df.columns:
        print("Ratio of missing " + col + ": {:.2f}"
              .format(sum(df[col].isna())/len(df)))
        
def print_tests_results(statistic, p_val, statistic_name, null_hyp, alpha=0.05):
    """
    Print the results of a statistical test

    Args:
        statistic: value of the computed statistic
        p_val: p-value
        statistic_name: string containing the name 
        of the statistic
        null_hyp: string containing the statement 
        of the null hypothesis
        alpha: significance level (default 0.05)

    """
    if p_val < alpha:
        print("With a value of {:.2f}".format(statistic), "for", statistic_name, 
                " and a p-value of {:.2f},".format(p_val), "\nwe CAN significantly "
                "REJECT the null hypothesis (i.e. \"", null_hyp, "\")")
    else:
        print("With a value of {:.2f}".format(statistic), "for", statistic_name, 
                " and a p-value of {:.2f},".format(p_val), "\nwe CANNOT significantly "
                "REJECT the null hypothesis (i.e. \"", null_hyp, "\")")