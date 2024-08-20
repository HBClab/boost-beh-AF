# run Quality Check against new sub data

import os
import sys
import pandas as pd
import seaborn as sb

def parse_cmd_args():
    import argparse
    parser = argparse.ArgumentParser(description='QC for AF')
    parser.add_argument('-s', type=str, help='Path to submission')
    parser.add_argument('-o', type=str, help='Path to output for QC plots and Logs')
    parser.add_argument('-sub', type=str, help='Subject ID')

    return parser.parse_args()

def df(submission):
    submission = pd.read_csv(submission)
    return submission

def qc(submission):
    # convert submission to DataFrame
    submission = df(submission)
     # check if submission is a DataFrame
    if not isinstance(submission, pd.DataFrame):
        raise ValueError('Submission is not a DataFrame. Could not run QC')
    # check if submission is empty
    if submission.empty:
        raise ValueError('Submission is empty')
    # check if submission has correct columns
    if not all(col in submission.columns for col in ['acc_sum','block','block_c','condition','correct','correct_response','datetime','endtime','flanker','jitter','project','response','response_test_buffer_response','response_test_target_response','response_time','response_time_test_buffer_response','response_time_test_target_response','row_sel','session_number','start_end','starttime','subject_id','target','task','task_vers','time_test_buffer','time_test_buffer_response','time_test_constants','time_test_flanker','time_test_jitter','time_test_logger','time_test_target','time_test_target_response','time_test_variables','trial']):
        raise ValueError('Submission is missing columns')
    # check if submission has correct number of rows (within 5% of expected = 145)
    if len(submission) < 137 or len(submission) > 153:
        raise ValueError('Submission has incorrect number of rows')
    
def plots(submission, output, sub):
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    import os
    from math import pi
    #load csv
    df = pd.read_csv(submission)

    #drop practice data
    test = df[df['block'] == 'test']
    def plot_circular_bar_graph(percentages, name, output_name):
        startangle = 90
        colors = ['#4393E5', '#43BAE5', '#7AE6EA', '#E5A443']
        
        # Convert data to fit the polar axis
        ys = [i *1.1 for i in range(len(percentages))]   # One bar for each block
        left = (startangle * pi * 2) / 360  # This is to control where the bar starts

        # Figure and polar axis
        fig, ax = plt.subplots(figsize=(6, 6))
        ax = plt.subplot(projection='polar')

        # Plot bars and points at the end to make them round
        for i, (block, percentage) in enumerate(percentages.items()):
            ax.barh(ys[i], percentage * 2 * pi, left=left, height=0.5, color=colors[i % len(colors)], label=block)
            ax.text(percentage + left + 0.02, ys[i], f'{percentage:.0%}', va='center', ha='left', color='black', fontsize=12)

        plt.ylim(-1, len(percentages))

        # Custom legend
        ax.legend(loc='center', frameon=True) 

        # Clear ticks and spines
        plt.xticks([])
        plt.yticks([])
        ax.spines.clear()
        plt.title(name, fontsize=15, pad=20, color="white")

        plt.savefig(os.path.join(output, f'{sub}_'+output_name+'.png'))
        plt.close()



    plt.figure(figsize=(10,6))
    sb.stripplot(x='condition', y='response_time', data=test, alpha=0.5)
    sb.boxplot(x='condition', y='response_time', data=test, whis=np.inf, linewidth=0.5)
    plt.savefig(os.path.join(output, f'{sub}_rt.png'))

    plot_circular_bar_graph(test['correct'].groupby(test['condition']).mean(), 'Accuracy by Condition', 'accuracy_by_condition')

 




def main():

    #parse command line arguments
    args = parse_cmd_args()
    submission = args.s
    output = args.o
    sub = args.sub

    # check if submission is a csv
    if not submission.endswith('.csv'):
        raise ValueError('Submission is not a csv')
    # check if submission exists
    if not os.path.exists(submission):
        raise ValueError('Submission does not exist')
    # run QC
    qc(submission)
    
    print(f'QC passed for {submission}, generating plots...')
    # generate plots
    plots(submission, output, sub)
    return submission
    
    
if __name__ == '__main__':
    main()

