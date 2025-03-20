"""Dialogs for result visualization."""

import logging
import os
from pathlib import Path

import FreeSimpleGUI as sg
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.cluster.hierarchy import leaves_list, linkage
from scipy.stats import zscore

from ccompass.core import ResultsModel
from ccompass.visualize import fig_to_bytes, fract_heatmap

logger = logging.getLogger(__package__)


def RP_gradient_heatmap(fract_data):
    """Create a GUI to display a heatmap with hierarchical clustering for each
    condition."""

    conditions = list(fract_data["vis"])

    # Define the layout
    layout = [
        [sg.Button("Export all")],
        [sg.Text("Select Condition:")],
        [
            sg.Combo(
                conditions,
                key="-CONDITION-",
                enable_events=True,
                readonly=True,
                default_value=None,
            )
        ],
        [sg.Image(key="-HEATMAP-")],
    ]

    window = sg.Window(
        "Hierarchical Clustering Heatmap",
        layout,
        finalize=True,
        resizable=True,
        modal=True,
    )

    # Function to plot heatmap and return as a PIL image
    def plot_heatmap(
        dataframe: pd.DataFrame,
        condition_name: str,
        save_as_pdf=False,
        folder_path=None,
    ):
        fract_heatmap(dataframe, title=f"Condition: {condition_name}")

        # If we need to save the plot as a PDF file
        if save_as_pdf and folder_path:
            pdf_filename = Path(folder_path, f"{condition_name}_heatmap.pdf")
            plt.savefig(pdf_filename, format="pdf")

    def export_results(fract_data, folder_path):
        """Export dataframes to Excel and heatmaps to PDFs."""
        Path(folder_path).mkdir(parents=True, exist_ok=True)

        # Create an Excel writer to save all conditions into one file
        excel_filename = os.path.join(folder_path, "conditions_data.xlsx")
        with pd.ExcelWriter(excel_filename, engine="xlsxwriter") as writer:
            # Loop through each condition and save the DataFrame
            for condition in fract_data["vis"]:
                df = fract_data["vis"][condition]
                df.to_excel(writer, sheet_name=condition)

                # Also generate and save the heatmap as a PDF
                plot_heatmap(
                    df,
                    condition_name=condition,
                    save_as_pdf=True,
                    folder_path=folder_path,
                )

        sg.popup(f"Export complete! Files saved in: {folder_path}")

    # Event loop
    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        # If a condition is selected from the dropdown menu
        if event == "-CONDITION-" and (
            selected_condition := values["-CONDITION-"]
        ):
            df = fract_data["vis"][selected_condition]

            # Generate the heatmap with hierarchical clustering and condition name as the title
            plot_heatmap(df, selected_condition)
            window["-HEATMAP-"].update(data=fig_to_bytes())

        # If the Export button is clicked
        elif event == "Export":
            # Open a folder selection window
            folder_path = sg.popup_get_folder("Select Folder")
            if folder_path:
                # Export the dataframes to Excel and the heatmaps to PDF
                export_results(fract_data, folder_path)

    window.close()


def RP_stats_heatmap(results: dict[str, ResultsModel]):
    """Create a GUI to display a heatmap with hierarchical clustering for each condition."""
    # Get the list of conditions from results
    conditions = list(results)

    layout = [
        [sg.Button("Export all")],
        [sg.Text("Select Condition:")],
        [
            sg.Combo(
                conditions,
                key="-CONDITION-",
                enable_events=True,
                readonly=True,
                default_value=None,
            )
        ],
        [sg.Image(key="-HEATMAP-")],
    ]

    # Create the window with a static size
    window = sg.Window(
        "Hierarchical Clustering Heatmap",
        layout,
        resizable=True,
        finalize=True,
        modal=True,
    )

    # Function to plot heatmap and return as a PIL image
    def plot_heatmap(
        dataframe, condition_name, save_as_pdf=False, folder_path=None
    ):
        # Filter out the columns that start with 'fCC_'
        fcc_columns = [
            col for col in dataframe.columns if col.startswith("fCC_")
        ]
        df_fcc = dataframe[fcc_columns]

        # Drop rows with NaN values
        df_fcc_cleaned = df_fcc.dropna()

        # Extract the column labels (the part after 'fCC_')
        x_labels = [col.replace("fCC_", "") for col in fcc_columns]

        # Perform hierarchical clustering on the rows
        linkage_matrix = linkage(df_fcc_cleaned, method="ward")
        clustered_rows = leaves_list(
            linkage_matrix
        )  # Order of rows after clustering

        # Reorder the DataFrame rows based on hierarchical clustering
        df_clustered = df_fcc_cleaned.iloc[clustered_rows, :]

        # Custom colormap: from #f2f2f2 (for value 0) to #6d6e71 (for value 1)
        cmap = mcolors.LinearSegmentedColormap.from_list(
            "custom_gray", ["#f2f2f2", "#6d6e71"], N=256
        )

        # Plot the heatmap using seaborn with the custom color gradient
        plt.figure(figsize=(8, 6))
        sns.heatmap(
            df_clustered,
            cmap=cmap,
            cbar=True,
            xticklabels=x_labels,
            yticklabels=False,
            vmin=0,
            vmax=1,
        )

        # Rotate the x-axis labels to be vertical
        plt.xticks(rotation=90)

        # Add the condition name as the title of the plot
        plt.title(f"Condition: {condition_name}", fontsize=16)

        plt.tight_layout()

        # If we need to save the plot as a PDF file
        if save_as_pdf and folder_path:
            pdf_filename = os.path.join(
                folder_path, f"{condition_name}_heatmap.pdf"
            )
            plt.savefig(pdf_filename, format="pdf")

    def export_results(results: dict[str, ResultsModel], folder_path):
        """Export dataframes to Excel and heatmaps to PDFs"""
        Path(folder_path).mkdir(parents=True, exist_ok=True)

        # Create an Excel writer to save all conditions into one file
        excel_filename = os.path.join(folder_path, "results_data.xlsx")

        with pd.ExcelWriter(excel_filename, engine="xlsxwriter") as writer:
            # Loop through each condition and save the 'metrics' DataFrame
            for condition, result in results.items():
                # Save the entire DataFrame to Excel
                result.metrics.to_excel(writer, sheet_name=condition)

                # Also generate and save the heatmap as a PDF using the fCC_ columns
                plot_heatmap(
                    result.metrics,
                    condition_name=condition,
                    save_as_pdf=True,
                    folder_path=folder_path,
                )

        sg.popup(f"Export complete! Files saved in: {folder_path}")

    # Event loop
    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        # If a condition is selected from the dropdown menu
        if event == "-CONDITION-" and (
            selected_condition := values["-CONDITION-"]
        ):
            df = results[selected_condition].metrics

            # Generate the heatmap with hierarchical clustering and condition name as the title
            plot_heatmap(df, selected_condition)
            window["-HEATMAP-"].update(data=fig_to_bytes())

        # If the Export button is clicked
        elif event == "Export":
            # Open a folder selection window
            folder_path = sg.popup_get_folder("Select Folder")
            if folder_path:
                # Export the dataframes to Excel and the heatmaps to PDF
                export_results(results, folder_path)

    # Close the window when done
    window.close()


def RP_stats_distribution(results: dict[str, ResultsModel]):
    conditions = list(results)

    # Define the layout
    layout = [
        [sg.Button("Export")],
        [sg.Text("Select Condition:")],
        [
            sg.Combo(
                conditions,
                key="-CONDITION-",
                enable_events=True,
                readonly=True,
                default_value=None,
            )
        ],
        [sg.Image(key="-PIECHART-")],
    ]

    # Create the window with a static size
    window = sg.Window(
        "Class Distribution Pie Chart",
        layout,
        resizable=True,
        finalize=True,
        modal=True,
    )

    # Function to plot pie chart and return as a PIL image
    def plot_pie_chart(
        dataframe, condition_name, save_as_pdf=False, folder_path=None
    ):
        # Get the 'fNN_winner' column
        fnn_winner = dataframe["fNN_winner"]

        # Calculate class distribution
        class_counts = fnn_winner.value_counts()

        # Create a pie chart
        plt.figure(figsize=(6, 6))
        # noinspection PyUnresolvedReferences
        plt.pie(
            class_counts,
            labels=class_counts.index,
            autopct="%1.1f%%",
            startangle=90,
            colors=plt.cm.Paired.colors,
        )
        plt.title(f"Class Distribution for {condition_name}")

        plt.tight_layout()

        # If we need to save the plot as a PDF file
        if save_as_pdf and folder_path:
            pdf_filename = os.path.join(
                folder_path, f"{condition_name}_piechart.pdf"
            )
            plt.savefig(pdf_filename, format="pdf")

    # Function to export pie charts and summary to Excel and PDFs
    def export_pie_charts(results: dict[str, ResultsModel], folder_path):
        Path(folder_path).mkdir(parents=True, exist_ok=True)

        # Create an Excel writer to save summary data
        excel_filename = os.path.join(
            folder_path, "class_distribution_summary.xlsx"
        )

        with pd.ExcelWriter(excel_filename, engine="xlsxwriter") as writer:
            # Loop through each condition and save the pie chart and class distribution
            for condition, result in results.items():
                # Rename 'fNN_winner' column to 'main organelle' before exporting
                df_export = result.metrics.rename(
                    columns={"fNN_winner": "main compartment"}
                )

                # Get the class distribution for 'main organelle'
                class_counts = df_export["main compartment"].value_counts()

                # Write the class counts to the Excel file
                class_counts.to_excel(writer, sheet_name=condition)

                # Save the pie chart for each condition as a PDF
                plot_pie_chart(
                    result.metrics,
                    condition_name=condition,
                    save_as_pdf=True,
                    folder_path=folder_path,
                )

        sg.popup(f"Export complete! Files saved in: {folder_path}")

    # Event loop
    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        # If a condition is selected from the dropdown menu
        if event == "-CONDITION-":
            selected_condition = values["-CONDITION-"]

            if selected_condition:
                df = results[selected_condition].metrics

                # Generate the pie chart for the class distribution
                plot_pie_chart(df, selected_condition)
                window["-PIECHART-"].update(data=fig_to_bytes())

        # If the Export button is clicked
        if event == "Export":
            # Open a folder selection window
            folder_path = sg.popup_get_folder("Select Folder")
            if folder_path:
                # Export the pie charts and the class distribution summary to Excel
                export_pie_charts(results, folder_path)

    # Close the window when done
    window.close()


def RP_global_heatmap(comparison):
    # Get the list of comparisons from the dictionary keys
    comparisons = list(comparison.keys())

    # Define the layout
    layout = [
        [sg.Button("Export all")],
        [sg.Text("Select Comparison:")],
        [
            sg.Combo(
                comparisons,
                key="-COMPARISON-",
                enable_events=True,
                readonly=True,
                default_value=None,
            )
        ],
        [sg.Image(key="-HEATMAP-")],
    ]

    # Create the window with a static size
    window = sg.Window(
        "Global Heatmap (Comparisons)",
        layout,
        resizable=True,
        finalize=True,
        modal=True,
    )

    # Custom colormap: from #730000 (for -1) to #f1f2f2 (for 0) to #1a0099 (for 1)
    cmap = mcolors.LinearSegmentedColormap.from_list(
        "custom_gradient", ["#730000", "#f1f2f2", "#1a0099"], N=256
    )

    # Function to filter the data based on the 'fRLS' column and get 'fRL_' columns only
    def filter_and_prepare_data(dataframe):
        # Keep only rows where 'fRLS' is greater than or equal to 1
        filtered_df = dataframe[dataframe["fRLS"] >= 1]

        # Filter out the columns that start with 'fRL_'
        frl_columns = [
            col for col in filtered_df.columns if col.startswith("fRL_")
        ]
        df_frl = filtered_df[frl_columns]

        # Rename columns from 'fRL_' to 'RL_'
        df_frl_renamed = df_frl.rename(
            columns=lambda col: col.replace("fRL_", "RL_")
        )

        return df_frl_renamed

    # Function to plot heatmap and return as a PIL image
    def plot_heatmap(
        dataframe, comparison_name, save_as_pdf=False, folder_path=None
    ):
        df_cleaned = dataframe.dropna()
        x_labels = dataframe.columns

        # Perform hierarchical clustering on the rows
        linkage_matrix = linkage(df_cleaned, method="ward")
        # Order of rows after clustering
        clustered_rows = leaves_list(linkage_matrix)
        # Reorder the DataFrame rows based on hierarchical clustering
        df_clustered = df_cleaned.iloc[clustered_rows, :]

        # Plot the heatmap using seaborn with the custom color gradient
        plt.figure(figsize=(8, 6))
        sns.heatmap(
            df_clustered,
            cmap=cmap,
            cbar=True,
            xticklabels=x_labels,
            yticklabels=False,
            vmin=-1,
            vmax=1,
        )

        # Rotate the x-axis labels to be vertical
        plt.xticks(rotation=90)
        plt.title(f"ReLocalizations: {comparison_name}", fontsize=16)
        plt.tight_layout()

        # If we need to save the plot as a PDF file
        if save_as_pdf and folder_path:
            pdf_filename = os.path.join(
                folder_path, f"{comparison_name}_heatmap.pdf"
            )
            plt.savefig(pdf_filename, format="pdf")

    def export_heatmaps(comparison, folder_path):
        """Export filtered and renamed dataframes to Excel and heatmaps to PDFs"""
        Path(folder_path).mkdir(parents=True, exist_ok=True)

        # Create an Excel writer to save all filtered data into one file
        excel_filename = os.path.join(
            folder_path, "filtered_comparison_data.xlsx"
        )

        with pd.ExcelWriter(excel_filename, engine="xlsxwriter") as writer:
            # Loop through each comparison and save the filtered and renamed DataFrame
            for comp in comparison:
                df = comparison[comp].metrics

                # Apply the filtering and renaming step for Excel export
                df_filtered = filter_and_prepare_data(df)

                # Write the filtered and renamed DataFrame to Excel
                df_filtered.to_excel(writer, sheet_name=str(comp))

                # Generate and save the heatmap as a PDF using the filtered data
                plot_heatmap(
                    df_filtered,
                    comparison_name=str(comp),
                    save_as_pdf=True,
                    folder_path=folder_path,
                )

        sg.popup(f"Export complete! Files saved in: {folder_path}")

    # Event loop
    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        # If a comparison is selected from the dropdown menu
        if event == "-COMPARISON-":
            selected_comparison = values["-COMPARISON-"]

            if selected_comparison:
                df = comparison[selected_comparison].metrics

                # Apply the filtering and renaming step for plotting
                df_filtered_for_plot = filter_and_prepare_data(df)

                # Generate the heatmap with hierarchical clustering and comparison name as the title
                plot_heatmap(df_filtered_for_plot, selected_comparison)
                window["-HEATMAP-"].update(data=fig_to_bytes())

        # If the Export button is clicked
        if event == "Export":
            # Open a folder selection window
            folder_path = sg.popup_get_folder("Select Folder")
            if folder_path:
                # Export the filtered dataframes to Excel and the heatmaps to PDF
                export_heatmaps(comparison, folder_path)

    # Close the window when done
    window.close()


def RP_global_distance(comparison):
    # Get the list of comparisons from the dictionary keys
    comparisons = list(comparison.keys())

    # Define the layout
    layout = [
        [sg.Button("Export")],
        [sg.Text("Select Comparison:")],
        [
            sg.Combo(
                comparisons,
                key="-COMPARISON-",
                enable_events=True,
                readonly=True,
                default_value=None,
            )
        ],
        [sg.Image(key="-SCATTERPLOT-")],
    ]

    window = sg.Window(
        "Global Distance Scatter Plot (Comparisons)",
        layout,
        resizable=True,
        finalize=True,
        modal=True,
    )

    def filter_data(dataframe):
        """Filter the data before plotting"""
        # Filter out rows where DS is 0 and where fRLS < 1
        filtered_df = dataframe[
            (dataframe["DS"] != 0) & (dataframe["fRLS"] >= 1)
        ]
        return filtered_df

    def plot_scatter(
        dataframe, comparison_name, save_as_pdf=False, folder_path=None
    ):
        """Create a scatter plot and return it as a PIL image"""
        # Filter the data
        filtered_df = filter_data(dataframe)

        # Get the x-axis (DS) and y-axis (P(t)_RLS, transformed to -log10)
        x_values = filtered_df["DS"]
        y_values = -np.log10(filtered_df["P(t)_RLS"])

        # Create the scatter plot
        plt.figure(figsize=(8, 6))
        plt.gca().set_facecolor("#f2f2f2")  # Set the background color

        # Determine colors for points based on whether they're above or below the line
        color_above_line = "#2200cc"
        color_below_line = "#990000"
        line_threshold = -np.log10(0.05)

        # Apply colors to points
        colors = np.where(
            y_values > line_threshold, color_above_line, color_below_line
        )

        # Plot the scatter points with the assigned colors
        plt.scatter(x_values, y_values, c=colors, alpha=0.7)

        # Plot the horizontal dashed line at y = -log10(0.05)
        plt.axhline(y=line_threshold, color="#6d6e71", linestyle="--")

        plt.xlabel("DS")
        plt.ylabel("-log10(P(t)_RLS)")
        plt.title(f"Distance Plot: {comparison_name}")

        plt.tight_layout()

        # If we need to save the plot as a PDF file
        if save_as_pdf and folder_path:
            pdf_filename = os.path.join(
                folder_path, f"{comparison_name}_scatterplot.pdf"
            )
            plt.savefig(pdf_filename, format="pdf")

    def export_scatter_data(comparison, folder_path):
        """Export scatter plot data and save to Excel and PDFs"""
        Path(folder_path).mkdir(parents=True, exist_ok=True)

        # Create an Excel writer to save all data into one file
        excel_filename = os.path.join(
            folder_path, "comparison_scatter_data.xlsx"
        )

        with pd.ExcelWriter(excel_filename, engine="xlsxwriter") as writer:
            # Loop through each comparison and save the filtered DataFrame
            for comp in comparison:
                df = comparison[comp].metrics

                # Filter the data before exporting
                df_filtered = filter_data(df)

                # Write the filtered DataFrame to Excel
                df_filtered[["DS", "P(t)_RLS"]].to_excel(
                    writer, sheet_name=str(comp)
                )

                # Generate and save the scatter plot as a PDF
                plot_scatter(
                    df_filtered,
                    comparison_name=str(comp),
                    save_as_pdf=True,
                    folder_path=folder_path,
                )

        sg.popup(f"Export complete! Files saved in: {folder_path}")

    # Event loop
    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        # If a comparison is selected from the dropdown menu
        if event == "-COMPARISON-":
            selected_comparison = values["-COMPARISON-"]

            if selected_comparison:
                df = comparison[selected_comparison].metrics

                # Generate the scatter plot with the selected comparison name
                plot_scatter(df, selected_comparison)
                window["-SCATTERPLOT-"].update(data=fig_to_bytes())

        # If the Export button is clicked
        if event == "Export":
            # Open a folder selection window
            folder_path = sg.popup_get_folder("Select Folder")
            if folder_path:
                # Export the scatter plot data and the plots to PDF
                export_scatter_data(comparison, folder_path)

    # Close the window when done
    window.close()


def RP_class_heatmap(results: dict[str, ResultsModel]):
    # Step 1: Get common classnames that are present in all conditions
    conditions = list(results.keys())
    classnames_lists = [
        set(results[condition].classnames) for condition in conditions
    ]

    # Find the intersection of classnames across all conditions
    common_classnames = list(set.intersection(*classnames_lists))

    # Define the layout
    layout = [
        [sg.Button("Export")],
        [sg.Text("Select Classname:")],
        [
            sg.Combo(
                common_classnames,
                key="-CLASSNAME-",
                enable_events=True,
                readonly=True,
                default_value=None,
            )
        ],
        [sg.Image(key="-HEATMAP-")],
    ]

    # Create the window with a static size
    window = sg.Window(
        "Class Clustering Heatmap",
        layout,
        resizable=True,
        finalize=True,
        modal=True,
    )

    def compute_rowwise_zscore(df):
        """Compute row-wise z-score."""
        # Ensure that rows with NaN values are removed before applying z-score
        return df.dropna(how="any").apply(zscore, axis=1)

    def ensure_numeric(df):
        """Ensure only numeric values are passed to clustering."""
        # Flatten any lists or arrays and ensure numeric values, forcing invalid parsing to NaN
        df_numeric = pd.DataFrame(df.tolist())  # Flatten lists into DataFrame
        df_numeric = df_numeric.apply(pd.to_numeric, errors="coerce")
        # Drop rows with any NaN values
        df_cleaned = df_numeric.dropna()
        return df_cleaned

    def filter_common_rows(df):
        """Filter rows that are present across all conditions (i.e., no NaNs across conditions)."""
        return df.dropna(how="any")

    def plot_heatmap(
        dataframe, classname, conditions, save_as_pdf=False, folder_path=None
    ):
        """Plot heatmap and return as a PIL image."""
        # Ensure the DataFrame contains only numeric values
        df_cleaned = ensure_numeric(dataframe)

        # Perform hierarchical clustering on the rows
        try:
            linkage_matrix = linkage(df_cleaned, method="ward")
            # Order of rows after clustering
            clustered_rows = leaves_list(linkage_matrix)
            # Reorder the DataFrame rows based on hierarchical clustering
            df_clustered = df_cleaned.iloc[clustered_rows, :]

            # Plot the heatmap using seaborn with the viridis colormap
            plt.figure(figsize=(8, 6))
            sns.heatmap(
                df_clustered,
                cmap="viridis",
                cbar=True,
                xticklabels=conditions,
                yticklabels=False,
            )

            plt.xticks(rotation=90)
            plt.title(f"Clustering Heatmap for {classname}", fontsize=16)

            plt.tight_layout()

            # If we need to save the plot as a PDF file
            if save_as_pdf and folder_path:
                pdf_filename = os.path.join(
                    folder_path, f"{classname}_heatmap.pdf"
                )
                plt.savefig(pdf_filename, format="pdf")

        except ValueError:
            logger.exception("Error during clustering")
            return None

    def export_heatmaps(
        results: dict[str, ResultsModel],
        common_classnames: list[str],
        folder_path,
    ):
        """Export heatmaps and data to PDF and Excel."""
        Path(folder_path).mkdir(parents=True, exist_ok=True)

        excel_filename = os.path.join(folder_path, "class_heatmap_data.xlsx")

        with pd.ExcelWriter(excel_filename, engine="xlsxwriter") as writer:
            # Loop through each common classname and generate the heatmap
            for classname in common_classnames:
                # Create a DataFrame where columns are conditions and rows are the values from 'nCPA_' + classname
                data_dict = {}
                for condition in conditions:
                    df_metrics = results[condition].metrics
                    column_name = f"nCPA_{classname}"
                    if column_name in df_metrics.columns:
                        data_dict[condition] = df_metrics[column_name]

                # Convert to DataFrame and filter rows that are present across all conditions
                df = pd.DataFrame(data_dict)

                # Remove rows with NaN values before exporting
                df_filtered = df.dropna(how="any")

                # Apply row-wise z-score transformation
                df_zscore = compute_rowwise_zscore(df_filtered)

                # Ensure the DataFrame contains only numeric values for Excel export
                df_numeric = df_zscore.apply(pd.to_numeric, errors="coerce")

                # Write the numeric z-scored DataFrame to Excel
                df_numeric.to_excel(writer, sheet_name=classname)

                # Generate the heatmap for this classname and save it as a PDF
                plot_heatmap(
                    df_numeric,
                    classname,
                    conditions,
                    save_as_pdf=True,
                    folder_path=folder_path,
                )

        sg.popup(f"Export complete! Files saved in: {folder_path}")

    # Event loop
    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        # If a classname is selected from the dropdown menu
        if event == "-CLASSNAME-":
            selected_classname = values["-CLASSNAME-"]

            if selected_classname:
                # Create a DataFrame where columns are conditions and rows are 'nCPA_' values for the selected classname
                data_dict = {}
                for condition in conditions:
                    df_metrics = results[condition].metrics
                    column_name = f"nCPA_{selected_classname}"
                    if column_name in df_metrics.columns:
                        data_dict[condition] = df_metrics[column_name]

                # Convert to DataFrame and filter rows that are present across all conditions
                df = pd.DataFrame(data_dict)
                df_filtered = filter_common_rows(df)

                # Apply row-wise z-score transformation
                df_zscore = compute_rowwise_zscore(df_filtered)

                # Generate the heatmap for the selected classname, using condition names as column labels
                plot_heatmap(df_zscore, selected_classname, conditions)

                window["-HEATMAP-"].update(data=fig_to_bytes())

        # If the Export button is clicked
        if event == "Export":
            # Open a folder selection window
            folder_path = sg.popup_get_folder("Select Folder")
            if folder_path:
                # Export the heatmaps and z-scored data to PDF and Excel
                export_heatmaps(results, common_classnames, folder_path)

    # Close the window when done
    window.close()
