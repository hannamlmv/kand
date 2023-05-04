from test_therese import main
def visualisation_redundancy():
    
    # Set the boolean parameter values based on preference
    display_barplot = False
    display_heatmap = False
    display_phylo = False
    print_unique_scores = False
    print_R_score = True
    # Call the main function with the desired parameter values
    main(display_barplot, display_heatmap, display_phylo, print_unique_scores, print_R_score)

visualisation_redundancy()

