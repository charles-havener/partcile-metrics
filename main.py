from plots import *
import pandas as pd
import os


def main():
    """Generates a series of charts and graphs to visualize particle count data
    """

    FILE_LOCATION = r'C:\Users\havenc\Documents\Environmental\Particle\data\master.xlsx'

    # Ensure that an images exists in the directory
    if not os.path.exists("images"):
        os.mkdir("images")

    # Read the excel file and get a list of all its sheets
    xl = pd.ExcelFile(FILE_LOCATION)
    sheets = xl.sheet_names

    # Loop through each tab to create charts for each functional area
    for group in sheets:
        # Ensure that folder paths are created to store images in an organized fashion
        if not os.path.exists("images\\" + group):
            os.mkdir("images\\" + group)

        # Create a data frame from the sheet and create/adjust some columns
        print("\nGenerating Dataframe for " + group)
        df = xl.parse(sheet_name=group, index_col=None, header=0)
        df['DATE'] = pd.to_datetime(df['DATE'])
        df["0.5 MICRONS"].replace(0,1,True) # 0s do not show on log scales
        df["5.0 MICRONS"].replace(0,1,True)

        # Create individual charts for each particle type
        for data_name in ["0.5 MICRONS", "5.0 MICRONS"]:
            print(f"\tCreating {data_name}  Single Bubble Charts for {group}")
            for days in [30]:
                output_name = f"Images/{group}/{group}-{data_name}-{days}_days"
                CreateSingleBubbleChart(df, output_name, data_name, group, days)
        
        # Create combo charts for the group
        print(f"\tCreating {data_name} Combo Bubble Charts for {group}")
        for days in [30]:
            data_name_1 = "0.5 MICRONS"
            data_name_2 = "5.0 MICRONS"
            output_name = f"Images/{group}/{group}-combo-{days}_days"
            CreateComboBubbleChart(df, output_name, data_name_1, data_name_2, group, days)


if __name__ == "__main__":
    main()