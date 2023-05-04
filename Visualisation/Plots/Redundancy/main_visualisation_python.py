from test_therese import main
def visualisation_redundancy():
    
    # Set the boolean parameter values based on preference
    display_barplot = True
    display_heatmap = False
    display_phylo = False
    print_unique_scores = True
    # Call the main function with the desired parameter values
    main(display_barplot, display_heatmap, display_phylo, print_unique_scores)

visualisation_redundancy()

